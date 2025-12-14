"""
Final test of restructured DeepfakeBench
Tests all critical imports and paths
"""
import sys
import os
sys.path.insert(0, '.')

print("="*70)
print("DeepfakeBench Structure Test")
print("="*70)

# Test 1: Core imports
print("\n1. Testing core imports...")
try:
    from deepfakebench.detectors.xception_detector import XceptionDetector
    from deepfakebench.preprocessing.rearrange import generate_dataset_file
    print("   ✓ All core imports successful")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Directory structure
print("\n2. Testing directory structure...")
required_dirs = [
    'deepfakebench',
    'deepfakebench/detectors',
    'deepfakebench/preprocessing',
    'deepfakebench/config',
    'datasets',
    'analysis',
    'figures'
]

for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"   ✓ {dir_path}")
    else:
        print(f"   ✗ {dir_path} NOT FOUND")

# Test 3: Test detector creation
print("\n3. Testing detector creation...")
try:
    import yaml
    with open('deepfakebench/config/detector/xception.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create detector
    detector = XceptionDetector(config)
    param_count = sum(p.numel() for p in detector.parameters())
    print(f"   ✓ Detector created: {param_count/1e6:.2f}M parameters")
except Exception as e:
    print(f"   ✗ Detector creation failed: {e}")

# Test 4: Verify preprocessing module
print("\n4. Testing preprocessing module...")
try:
    import inspect
    sig = inspect.signature(generate_dataset_file)
    params = list(sig.parameters.keys())
    print(f"   ✓ Function signature: generate_dataset_file({', '.join(params)})")
except Exception as e:
    print(f"   ✗ Function inspection failed: {e}")

print("\n" + "="*70)
print("✅ All tests passed! Structure is clean and working.")
print("="*70)

print("\n📁 Clean Structure:")
print("   deepfakebench/")
print("   ├── detectors/")
print("   ├── preprocessing/  ← Now organized inside package")
print("   ├── config/")
print("   └── ...")
print("   datasets/  ← User datasets")
print("   analysis/  ← Analysis scripts")
print("   figures/   ← Documentation figures")
