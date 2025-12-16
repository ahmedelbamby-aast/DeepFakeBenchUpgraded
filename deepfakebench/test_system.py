#!/usr/bin/env python3
"""
DeepFakeBench System Test Script
================================

This script performs comprehensive testing of the DeepFakeBench system.
Run this after installation to verify everything is working correctly.

Usage:
    python -m deepfakebench.test_system
    python deepfakebench/test_system.py
"""

import sys
import os
import warnings

# Add parent directory to path for local testing
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")


def print_section(text):
    print(f"\n{Colors.BOLD}[{text}]{Colors.END}")


def print_pass(text):
    print(f"  {Colors.GREEN}✓{Colors.END} {text}")


def print_fail(text, error=None):
    print(f"  {Colors.RED}✗{Colors.END} {text}")
    if error:
        print(f"    {Colors.RED}Error: {error}{Colors.END}")


def print_warn(text):
    print(f"  {Colors.YELLOW}⚠{Colors.END} {text}")


def test_imports():
    """Test core module imports."""
    print_section("Testing Core Imports")
    
    results = []
    
    # Test main module
    try:
        import deepfakebench
        print_pass("deepfakebench")
        results.append(True)
    except Exception as e:
        print_fail("deepfakebench", str(e))
        results.append(False)
    
    # Test submodules
    submodules = [
        ("deepfakebench.config", "ConfigManager"),
        ("deepfakebench.detectors", "DETECTOR"),
        ("deepfakebench.networks", "BACKBONE"),
        ("deepfakebench.dataset", "DeepfakeAbstractBaseDataset"),
        ("deepfakebench.trainer.trainer", "Trainer"),
        ("deepfakebench.metrics", None),
        ("deepfakebench.loss", None),
        ("deepfakebench.preprocessing", None),
    ]
    
    for module_name, attr in submodules:
        try:
            module = __import__(module_name, fromlist=[attr] if attr else [])
            if attr:
                getattr(module, attr)
            print_pass(module_name)
            results.append(True)
        except Exception as e:
            print_fail(module_name, str(e))
            results.append(False)
    
    return all(results), results


def test_detectors():
    """Test detector loading."""
    print_section("Testing Detectors")
    
    results = []
    
    try:
        from deepfakebench.detectors import DETECTOR
        
        detector_count = len(DETECTOR.data)
        print_pass(f"Loaded {detector_count} detectors")
        results.append(True)
        
        # List some detectors
        detectors = list(DETECTOR.data.keys())
        print(f"    Available: {', '.join(detectors[:5])}...")
        
        # Test a few key detectors
        key_detectors = ['xception', 'efficientnetb4', 'clip', 'meso4']
        for name in key_detectors:
            if name in DETECTOR.data:
                cls = DETECTOR.data[name]
                print_pass(f"Detector '{name}' -> {cls.__name__}")
                results.append(True)
            else:
                print_fail(f"Detector '{name}' not found")
                results.append(False)
    
    except Exception as e:
        print_fail("Failed to load detectors", str(e))
        results.append(False)
    
    return all(results), results


def test_networks():
    """Test network/backbone loading."""
    print_section("Testing Networks/Backbones")
    
    results = []
    
    try:
        from deepfakebench.networks import BACKBONE
        
        if hasattr(BACKBONE, 'data'):
            backbone_count = len(BACKBONE.data)
            print_pass(f"Loaded {backbone_count} backbones")
            backbones = list(BACKBONE.data.keys())
            print(f"    Available: {', '.join(backbones)}")
        else:
            print_pass("BACKBONE registry loaded")
        results.append(True)
    
    except Exception as e:
        print_fail("Failed to load networks", str(e))
        results.append(False)
    
    return all(results), results


def test_config():
    """Test configuration system."""
    print_section("Testing Configuration System")
    
    results = []
    
    try:
        from deepfakebench.config import ConfigManager
        
        cm = ConfigManager()
        print_pass(f"ConfigManager initialized")
        print(f"    Project root: {cm.paths.project_root}")
        results.append(True)
        
        # Test path attributes
        path_attrs = ['datasets', 'logs', 'checkpoints', 'pretrained_dir']
        for attr in path_attrs:
            if hasattr(cm.paths, attr):
                print_pass(f"Path: {attr} = {getattr(cm.paths, attr)}")
                results.append(True)
            else:
                print_fail(f"Missing path attribute: {attr}")
                results.append(False)
        
        # Test hardware config
        print_pass(f"Hardware device: {cm.hardware.get_device()}")
        results.append(True)
        
    except Exception as e:
        print_fail("ConfigManager failed", str(e))
        results.append(False)
    
    return all(results), results


def test_yaml_configs():
    """Test YAML config file loading."""
    print_section("Testing YAML Config Files")
    
    results = []
    
    import yaml
    from pathlib import Path
    
    config_dir = Path(__file__).parent / "config"
    
    # Test main configs
    for config_name in ['train_config.yaml', 'test_config.yaml']:
        config_path = config_dir / config_name
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                print_pass(f"Loaded {config_name}")
                results.append(True)
                
                # Check for absolute paths
                has_absolute = False
                for key, value in config.items():
                    if isinstance(value, str) and value.startswith('/'):
                        has_absolute = True
                        print_warn(f"  Absolute path in {key}: {value[:40]}...")
                
                if not has_absolute:
                    print(f"    All paths are relative ✓")
                    
            except Exception as e:
                print_fail(f"Failed to load {config_name}", str(e))
                results.append(False)
        else:
            print_warn(f"{config_name} not found")
    
    # Check detector configs
    detector_config_dir = config_dir / "detector"
    if detector_config_dir.exists():
        configs = list(detector_config_dir.glob("*.yaml"))
        print_pass(f"Found {len(configs)} detector configs")
        results.append(True)
    
    return all(results), results


def test_pytorch():
    """Test PyTorch installation."""
    print_section("Testing PyTorch")
    
    results = []
    
    try:
        import torch
        print_pass(f"PyTorch version: {torch.__version__}")
        results.append(True)
        
        # Check CUDA
        if torch.cuda.is_available():
            print_pass(f"CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"    CUDA version: {torch.version.cuda}")
        else:
            print_warn("CUDA not available (CPU only)")
        results.append(True)
        
        # Test basic tensor operations
        x = torch.randn(2, 3)
        y = torch.randn(3, 2)
        z = torch.matmul(x, y)
        print_pass("Tensor operations OK")
        results.append(True)
        
    except Exception as e:
        print_fail("PyTorch test failed", str(e))
        results.append(False)
    
    return all(results), results


def test_dependencies():
    """Test key dependencies."""
    print_section("Testing Key Dependencies")
    
    results = []
    
    dependencies = [
        ("numpy", None),
        ("scipy", None),
        ("sklearn", "scikit-learn"),
        ("cv2", "opencv"),
        ("PIL", "Pillow"),
        ("albumentations", None),
        ("timm", None),
        ("kornia", None),
        ("transformers", None),
        ("tensorboard", None),
        ("einops", None),
        ("lmdb", None),
        ("dlib", "dlib-bin"),
    ]
    
    for import_name, display_name in dependencies:
        display = display_name or import_name
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print_pass(f"{display}: {version}")
            results.append(True)
        except ImportError:
            print_fail(f"{display}: not installed")
            results.append(False)
    
    return all(results), results


def test_cli():
    """Test command-line interface."""
    print_section("Testing CLI Scripts")
    
    results = []
    
    # Test train.py imports
    try:
        import sys
        from pathlib import Path
        
        # Add parent to path
        deepfakebench_dir = Path(__file__).parent
        
        # Check if train.py exists
        train_path = deepfakebench_dir / "train.py"
        test_path = deepfakebench_dir / "test.py"
        
        if train_path.exists():
            print_pass("train.py exists")
            results.append(True)
        else:
            print_fail("train.py not found")
            results.append(False)
        
        if test_path.exists():
            print_pass("test.py exists")
            results.append(True)
        else:
            print_fail("test.py not found")
            results.append(False)
            
    except Exception as e:
        print_fail("CLI test failed", str(e))
        results.append(False)
    
    return all(results), results


def main():
    """Run all tests."""
    print_header("DeepFakeBench System Test")
    print(f"Python version: {sys.version}")
    
    all_results = []
    
    # Run all tests
    tests = [
        ("Core Imports", test_imports),
        ("Detectors", test_detectors),
        ("Networks", test_networks),
        ("Configuration", test_config),
        ("YAML Configs", test_yaml_configs),
        ("PyTorch", test_pytorch),
        ("Dependencies", test_dependencies),
        ("CLI Scripts", test_cli),
    ]
    
    for test_name, test_func in tests:
        try:
            passed, results = test_func()
            all_results.extend(results)
        except Exception as e:
            print_fail(f"{test_name} test crashed", str(e))
            all_results.append(False)
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for r in all_results if r)
    failed = sum(1 for r in all_results if not r)
    total = len(all_results)
    
    print(f"\n  Total tests: {total}")
    print(f"  {Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"  {Colors.RED}Failed: {failed}{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed! ✓{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}Some tests failed. Review the output above.{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
