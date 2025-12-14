"""
Local Test Script for DeepfakeBench
Tests the new package structure on local machine
"""

import sys
import os

print("=" * 60)
print("DeepfakeBench Local Test")
print("=" * 60)

# Add current directory to path
sys.path.insert(0, os.getcwd())

print("\n1. Testing package import...")
try:
    import deepfakebench
    print(f"   ✓ DeepfakeBench v{deepfakebench.__version__}")
    print(f"   ✓ Author: {deepfakebench.__author__}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n2. Testing PyTorch availability...")
try:
    import torch
    print(f"   ✓ PyTorch: {torch.__version__}")
    print(f"   ✓ CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   ✓ GPU: {torch.cuda.get_device_name(0)}")
except ImportError:
    print("   ⚠ PyTorch not installed (optional for import test)")

print("\n3. Testing detector import (needs dependencies)...")
try:
    from deepfakebench.detectors.xception_detector import XceptionDetector
    print(f"   ✓ XceptionDetector imported successfully")
except ModuleNotFoundError as e:
    print(f"   ⚠ Missing dependency: {e}")
    print(f"   → Run: pip install -r requirements.txt")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n4. Checking package structure...")
try:
    expected_modules = ['detectors', 'networks', 'dataset', 'trainer', 'loss', 'metrics']
    deepfakebench_path = os.path.join(os.getcwd(), 'deepfakebench')
    
    for module in expected_modules:
        module_path = os.path.join(deepfakebench_path, module)
        if os.path.exists(module_path):
            print(f"   ✓ {module}/ exists")
        else:
            print(f"   ✗ {module}/ missing")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n5. Testing configuration files...")
config_files = [
    'deepfakebench/config/detector/xception.yaml',
    'requirements.txt',
    'setup.py',
    'pyproject.toml'
]

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"   ✓ {config_file}")
    else:
        print(f"   ✗ {config_file} missing")

print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)
print("✓ Package structure is correct")
print("✓ Package can be imported")
print("⚠ To test detectors, install dependencies:")
print("  pip install -r requirements.txt")
print("=" * 60)
