# Kaggle Testing Guide

## Quick Start - Run these cells in Kaggle Notebook

### Cell 1: Clone Repository
```python
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
```

### Cell 2: Install Dependencies
```python
!bash kaggle_install.sh
```

### Cell 3: Import Test (Simple)
```python
import sys
sys.path.insert(0, '/kaggle/working/DeepFakeBenchUpgraded')

# Test basic imports
print("Testing imports...")
import deepfakebench
print(f"✓ Package version: {deepfakebench.__version__}")

# Test detector import
from deepfakebench.detectors.sladd_detector import SLADDXceptionDetector
print("✓ Successfully imported SLADDXceptionDetector")
```

### Cell 4: Create Detector with Minimal Config
```python
import torch

# Minimal config for testing (no training/dataset required)
config = {
    'backbone_name': 'xception_sladd',
    'backbone_config': {
        'mode': 'original',
        'num_classes': 2,
        'inc': 3,
        'dropout': False
    },
    'pretrained': 'None',  # No pretrained weights for quick test
    'loss_func': 'cross_entropy',
    'typeloss_func': 'am_softmax',  # Required for SLADD
    'optimizer': {
        'adam': {
            'lr': 0.0002,
            'beta1': 0.9,
            'weight_decay': 0.0005
        }
    }
}

# Create detector instance
print("Creating detector...")
detector = SLADDXceptionDetector(config)
print(f"✓ Detector created successfully")
print(f"✓ Device: {next(detector.parameters()).device}")
print(f"✓ Model has {sum(p.numel() for p in detector.parameters())/1e6:.2f}M parameters")

# Test feature extraction with dummy input
dummy_input = torch.randn(1, 3, 256, 256)
with torch.no_grad():
    features = detector.features(dummy_input)
    if isinstance(features, tuple):
        features = features[0]  # SLADD returns (features, intermediate)
print(f"✓ Feature extraction successful, output shape: {features.shape}")
```

## Alternative: Full Configuration Test

### Cell 4b: Load from YAML Config (Optional)
```python
import yaml
import torch

# Load full config from file
with open('deepfakebench/config/detector/sladd_detector.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Override paths for Kaggle environment
config['pretrained'] = 'None'  # Skip pretrained weights for quick test
config['log_dir'] = './kaggle_logs'

print("Config loaded:")
print(f"  Model: {config['model_name']}")
print(f"  Backbone: {config['backbone_name']}")

# Create detector
detector = SLADDXceptionDetector(config)
print(f"✓ Detector created with full config")
```

## Expected Output

✅ All cells should run without errors  
✅ Import test shows package version 2.0.0  
✅ Detector creation succeeds  
✅ Forward pass produces output  

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'X'`  
**Solution**: The package X is missing. Check kaggle_install.sh and ensure it's installed.

**Issue**: `TypeError: __init__() missing required positional argument: 'config'`  
**Solution**: Use Cell 4 above - detectors require a config dictionary.

**Issue**: `AssertionError: Torch not compiled with CUDA enabled`  
**Solution**: This is now handled gracefully. The code will work on CPU if GPU is not available.

**Issue**: `RuntimeError: Unable to open dlib model file`  
**Solution**: This is now lazy-loaded. The error only occurs if you actually use FWA blending features.
