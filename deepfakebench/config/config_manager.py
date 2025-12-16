"""
DeepFakeBench Configuration Management System
==============================================

Provides a unified, dynamic configuration system that:
- Supports multiple configuration sources (YAML, environment variables, CLI)
- Handles path resolution automatically
- Validates configuration values
- Provides sensible defaults
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field
from copy import deepcopy

logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """
    Dynamically determine the project root directory.
    Works regardless of where the script is called from.
    """
    # Start from this file's location
    current = Path(__file__).resolve()
    
    # Walk up until we find pyproject.toml or setup.py
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() or (parent / "setup.py").exists():
            return parent
    
    # Fallback to current working directory
    return Path.cwd()


# Project root path (computed once)
PROJECT_ROOT = get_project_root()


@dataclass
class PathConfig:
    """Path configuration with automatic resolution."""
    project_root: Path = field(default_factory=lambda: PROJECT_ROOT)
    datasets: Path = field(default_factory=lambda: PROJECT_ROOT / "datasets")
    rgb_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "datasets" / "rgb")
    lmdb_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "datasets" / "lmdb")
    data_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "datasets")
    checkpoints: Path = field(default_factory=lambda: PROJECT_ROOT / "checkpoints")
    logs: Path = field(default_factory=lambda: PROJECT_ROOT / "logs")
    outputs: Path = field(default_factory=lambda: PROJECT_ROOT / "outputs")
    cache: Path = field(default_factory=lambda: PROJECT_ROOT / "cache")
    pretrained_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "deepfakebench" / "pretrained")
    pretrained: Path = field(default_factory=lambda: PROJECT_ROOT / "deepfakebench" / "pretrained")
    configs: Path = field(default_factory=lambda: PROJECT_ROOT / "deepfakebench" / "config")


@dataclass
class HardwareConfig:
    """Hardware configuration."""
    device: str = "auto"  # auto, cuda, cpu, mps
    num_workers: int = 4
    pin_memory: bool = True
    mixed_precision: bool = True
    
    def get_device(self) -> str:
        """Get the actual device to use."""
        if self.device == "auto":
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        return self.device


@dataclass
class TrainingConfig:
    """Training configuration defaults."""
    batch_size: int = 32
    learning_rate: float = 0.0002
    epochs: int = 50
    save_frequency: int = 5
    log_frequency: int = 100
    early_stopping_patience: int = 10
    gradient_clip: float = 1.0


@dataclass
class InferenceConfig:
    """Inference configuration defaults."""
    batch_size: int = 64
    save_predictions: bool = True
    save_visualizations: bool = False


class ConfigManager:
    """
    Central configuration manager for DeepFakeBench.
    
    Usage:
        config = ConfigManager()
        config.load("path/to/config.yaml")
        
        # Access configuration
        print(config.paths.datasets)
        print(config.hardware.device)
        print(config["model_name"])  # Dictionary-style access
    """
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.project_root = PROJECT_ROOT
        self.paths = PathConfig()
        self.hardware = HardwareConfig()
        self.training = TrainingConfig()
        self.inference = InferenceConfig()
        self._custom_config: Dict[str, Any] = {}
        
        # Load configuration if provided
        if config_path:
            self.load(config_path)
        
        # Load local config if exists
        local_config = PROJECT_ROOT / "config" / "local_config.yaml"
        if local_config.exists():
            self._load_local_config(local_config)
        
        # Override with environment variables
        self._load_env_vars()
    
    def load(self, config_path: Union[str, Path]) -> "ConfigManager":
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            Self for chaining
        """
        config_path = Path(config_path)
        
        if not config_path.is_absolute():
            # Try relative to project root
            config_path = self.project_root / config_path
        
        if not config_path.exists():
            # Try relative to config directory
            config_path = self.paths.configs / config_path.name
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
        
        self._merge_config(data)
        logger.info(f"Loaded configuration from {config_path}")
        
        return self
    
    def _load_local_config(self, path: Path) -> None:
        """Load local configuration overrides."""
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f) or {}
            self._merge_config(data)
            logger.debug(f"Loaded local configuration from {path}")
        except Exception as e:
            logger.warning(f"Failed to load local config: {e}")
    
    def _load_env_vars(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            "DEEPFAKEBENCH_DEVICE": ("hardware", "device"),
            "DEEPFAKEBENCH_BATCH_SIZE": ("training", "batch_size"),
            "DEEPFAKEBENCH_NUM_WORKERS": ("hardware", "num_workers"),
            "DEEPFAKEBENCH_DATASETS_DIR": ("paths", "datasets"),
            "DEEPFAKEBENCH_CHECKPOINTS_DIR": ("paths", "checkpoints"),
            "DEEPFAKEBENCH_LOGS_DIR": ("paths", "logs"),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                self._set_nested(section, key, value)
                logger.debug(f"Set {section}.{key} from {env_var}")
    
    def _merge_config(self, data: Dict[str, Any]) -> None:
        """Merge configuration dictionary."""
        # Merge paths
        if "paths" in data:
            for key, value in data["paths"].items():
                if hasattr(self.paths, key):
                    setattr(self.paths, key, self._resolve_path(value))
        
        # Merge hardware
        if "hardware" in data:
            for key, value in data["hardware"].items():
                if hasattr(self.hardware, key):
                    setattr(self.hardware, key, value)
        
        # Merge training
        if "training" in data:
            for key, value in data["training"].items():
                if hasattr(self.training, key):
                    setattr(self.training, key, value)
        
        # Merge inference
        if "inference" in data:
            for key, value in data["inference"].items():
                if hasattr(self.inference, key):
                    setattr(self.inference, key, value)
        
        # Store remaining custom config
        for key, value in data.items():
            if key not in ["paths", "hardware", "training", "inference"]:
                self._custom_config[key] = value
    
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """Resolve path relative to project root."""
        path = Path(path)
        if not path.is_absolute():
            path = self.project_root / path
        return path.resolve()
    
    def _set_nested(self, section: str, key: str, value: Any) -> None:
        """Set a nested configuration value."""
        section_obj = getattr(self, section, None)
        if section_obj and hasattr(section_obj, key):
            # Type conversion
            current_value = getattr(section_obj, key)
            if isinstance(current_value, bool):
                value = value.lower() in ("true", "1", "yes")
            elif isinstance(current_value, int):
                value = int(value)
            elif isinstance(current_value, float):
                value = float(value)
            elif isinstance(current_value, Path):
                value = self._resolve_path(value)
            setattr(section_obj, key, value)
    
    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access to custom config."""
        return self._custom_config.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Dictionary-style setting of custom config."""
        self._custom_config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a custom config value with default."""
        return self._custom_config.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire configuration to dictionary."""
        return {
            "project_root": str(self.project_root),
            "paths": {
                k: str(v) for k, v in vars(self.paths).items()
            },
            "hardware": vars(self.hardware),
            "training": vars(self.training),
            "inference": vars(self.inference),
            **self._custom_config
        }
    
    def save(self, path: Union[str, Path]) -> None:
        """Save current configuration to YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)
        
        logger.info(f"Configuration saved to {path}")
    
    def ensure_directories(self) -> None:
        """Create all configured directories if they don't exist."""
        for name in ["datasets", "checkpoints", "logs", "outputs", "cache"]:
            path = getattr(self.paths, name)
            path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.paths.datasets / "rgb").mkdir(parents=True, exist_ok=True)
        (self.paths.datasets / "lmdb").mkdir(parents=True, exist_ok=True)
        
        logger.info("Created directory structure")


# Global configuration instance
_global_config: Optional[ConfigManager] = None


def get_config(config_path: Optional[Union[str, Path]] = None) -> ConfigManager:
    """
    Get the global configuration instance.
    
    Args:
        config_path: Optional path to load configuration from
        
    Returns:
        ConfigManager instance
    """
    global _global_config
    
    if _global_config is None or config_path is not None:
        _global_config = ConfigManager(config_path)
    
    return _global_config


def reset_config() -> None:
    """Reset the global configuration instance."""
    global _global_config
    _global_config = None


# Convenience exports
__all__ = [
    "ConfigManager",
    "PathConfig", 
    "HardwareConfig",
    "TrainingConfig",
    "InferenceConfig",
    "get_config",
    "reset_config",
    "PROJECT_ROOT",
    "get_project_root",
]
