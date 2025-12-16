"""
DeepFakeBench Configuration Module
==================================

Provides unified configuration management for the entire project.
"""

import os
import sys

# Dynamic path setup
current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_file_path))
project_root_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)
sys.path.append(project_root_dir)

# Import configuration manager
from .config_manager import (
    ConfigManager,
    PathConfig,
    HardwareConfig,
    TrainingConfig,
    InferenceConfig,
    get_config,
    reset_config,
    PROJECT_ROOT,
    get_project_root,
)

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
