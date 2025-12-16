# 🔧 Troubleshooting Guide

> Solutions to common issues and technical problems

---

## 📋 Table of Contents

- [Installation Issues](#installation-issues)
- [Import Errors](#import-errors)
- [Runtime Errors](#runtime-errors)
- [Performance Issues](#performance-issues)
- [Dataset Issues](#dataset-issues)
- [Warning Suppression](#warning-suppression)
- [Optional Dependencies](#optional-dependencies)

---

## Installation Issues

### Issue: Dependencies Conflict

**Problem**: Version conflicts during installation
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solution 1**: Use Kaggle installer (recommended for Kaggle)
```bash
bash kaggle_install.sh
```

**Solution 2**: Install with --no-deps flag
```bash
pip install --no-deps opencv-python
pip install --no-deps albumentations
pip install --no-deps imgaug
```

**Solution 3**: Create clean virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Missing CUDA

**Problem**: PyTorch not detecting GPU
```
CUDA not available, using CPU
```

**Solution**: Install PyTorch with CUDA support
```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Verification**:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"PyTorch version: {torch.__version__}")
```

### Issue: Slow Installation

**Problem**: Installation takes too long

**Solution**: Use binary wheels and skip unnecessary packages
```bash
# Use --no-cache-dir to force fresh downloads
pip install --no-cache-dir -r requirements.txt

# Or install only core dependencies
pip install torch opencv-python scikit-learn pyyaml lmdb
```

---

## Import Errors

### Issue: ModuleNotFoundError

**Problem**: Cannot import deepfakebench modules
```python
ModuleNotFoundError: No module named 'deepfakebench'
```

**Solution 1**: Add to Python path
```python
import sys
sys.path.insert(0, '/path/to/DeepFakeBenchUpgraded')
# Now imports will work
from deepfakebench.detectors import XceptionDetector
```

**Solution 2**: Install as package
```bash
cd DeepFakeBenchUpgraded
pip install -e .
# Now can import from anywhere
```

**Solution 3**: Set PYTHONPATH
```bash
export PYTHONPATH="/path/to/DeepFakeBenchUpgraded:$PYTHONPATH"
```

### Issue: Import Path Errors

**Problem**: Old-style imports don't work
```python
from detectors.xception_detector import XceptionDetector  # Error!
```

**Solution**: Use correct import paths
```python
# Correct way
from deepfakebench.detectors.xception_detector import XceptionDetector
```

**Why it changed**: Package was restructured from `training/` to `deepfakebench/`

### Issue: Circular Import

**Problem**: Circular import detected

**Solution**: Check import order and use lazy imports
```python
# Instead of importing at top
from deepfakebench.detectors import DETECTOR

# Use lazy import
def get_detector():
    from deepfakebench.detectors import DETECTOR
    return DETECTOR
```

---

## Runtime Errors

### Issue: CUDA Out of Memory (OOM)

**Problem**: GPU runs out of memory
```
RuntimeError: CUDA out of memory. Tried to allocate X MiB
```

**Solution 1**: Reduce batch size
```python
# In config YAML
batch_size: 16  # Reduce from 32
```

**Solution 2**: Enable gradient checkpointing
```python
# In model definition
torch.utils.checkpoint.checkpoint(layer, x)
```

**Solution 3**: Use mixed precision training
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
with autocast():
    output = model(input)
```

**Solution 4**: Clear cache
```python
import torch
torch.cuda.empty_cache()
```

**Solution 5**: Monitor memory usage
```python
import torch
print(f"Allocated: {torch.cuda.memory_allocated()/1e9:.2f} GB")
print(f"Reserved: {torch.cuda.memory_reserved()/1e9:.2f} GB")
```

### Issue: NumPy Deprecated Types

**Problem**: NumPy type errors
```
AttributeError: module 'numpy' has no attribute 'int'
```

**Solution**: Already fixed in v2.0.0! Update to latest version.

**If you see this error**:
```bash
git pull origin main
# Ensure you're using v2.0.0 or later
```

**Manual fix** (if needed):
```python
# Old (deprecated)
x = np.int(5)
y = np.float(3.14)

# New (correct)
x = int(5)
y = float(3.14)
```

### Issue: Model Loading Errors

**Problem**: Cannot load pretrained weights
```
RuntimeError: Error(s) in loading state_dict
```

**Solution 1**: Check model architecture matches
```python
# Ensure config matches saved model
config['backbone_name'] = 'xception'  # Must match
```

**Solution 2**: Use strict=False for partial loading
```python
model.load_state_dict(checkpoint, strict=False)
```

**Solution 3**: Verify checkpoint path
```python
import os
ckpt_path = './weights/model.pth'
print(f"Checkpoint exists: {os.path.exists(ckpt_path)}")
```

**Solution 4**: Use 'None' for no pretrained weights
```python
config['pretrained'] = 'None'  # String, not Python None
```

---

## Performance Issues

### Issue: Slow Data Loading

**Problem**: Training bottlenecked by data loading

**Solution 1**: Use LMDB format
```python
# Convert dataset to LMDB
from deepfakebench.preprocessing.dataset2lmdb import convert_to_lmdb

convert_to_lmdb(
    json_path='./dataset_json/FaceForensics++.json',
    output_path='./lmdb',
    compression='c23'
)
```

**Solution 2**: Increase num_workers
```python
# In config
num_workers: 8  # Increase based on CPU cores
```

**Solution 3**: Use pin_memory
```python
DataLoader(dataset, batch_size=32, pin_memory=True)
```

**Solution 4**: Enable persistent workers
```python
DataLoader(dataset, batch_size=32, persistent_workers=True)
```

### Issue: Slow Training

**Problem**: Training takes too long

**Solution 1**: Use mixed precision
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
for data in dataloader:
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

**Solution 2**: Use DataParallel for multi-GPU
```python
if torch.cuda.device_count() > 1:
    model = nn.DataParallel(model)
```

**Solution 3**: Use DistributedDataParallel
```bash
# Use train.sh for DDP
bash train.sh
```

**Solution 4**: Profile to find bottlenecks
```python
import torch.profiler as profiler

with profiler.profile(
    activities=[profiler.ProfilerActivity.CPU, profiler.ProfilerActivity.CUDA]
) as prof:
    # Your training code
    pass

print(prof.key_averages().table(sort_by="cuda_time_total"))
```

---

## Dataset Issues

### Issue: Dataset Not Found

**Problem**: Cannot load dataset
```
FileNotFoundError: Dataset path does not exist
```

**Solution 1**: Verify dataset path
```python
import os
dataset_path = '/kaggle/input/your-dataset'
print(f"Exists: {os.path.exists(dataset_path)}")
print(f"Contents: {os.listdir(dataset_path)}")
```

**Solution 2**: Check JSON mapping
```python
import json
with open('./dataset_json/FaceForensics++.json', 'r') as f:
    dataset_info = json.load(f)
print(f"Total videos: {len(dataset_info)}")
```

**Solution 3**: Generate JSON mapping
```python
from deepfakebench.preprocessing.rearrange import generate_dataset_file

generate_dataset_file(
    dataset_name='FaceForensics++',
    dataset_root_path='/path/to/dataset',
    output_file_path='./dataset_json/FaceForensics++.json',
    compression_level='c23'
)
```

### Issue: Wrong Dataset Structure

**Problem**: Dataset structure doesn't match expected format

**Solution**: Check structure matches this format:
```
FaceForensics++/
├── manipulated_sequences/
│   ├── Face2Face/c23/frames/[videos]/[frames.png]
│   ├── Deepfakes/c23/frames/[videos]/[frames.png]
│   └── ...
└── original_sequences/
    └── youtube/c23/frames/[videos]/[frames.png]
```

**Verify structure**:
```python
import os

base_path = '/path/to/FaceForensics++'
manip_path = os.path.join(base_path, 'manipulated_sequences')

# Check manipulation methods
methods = os.listdir(manip_path)
print(f"Found methods: {methods}")

# Check one method's structure
method_path = os.path.join(manip_path, methods[0], 'c23', 'frames')
print(f"Frames path exists: {os.path.exists(method_path)}")
```

### Issue: Empty Dataset

**Problem**: Dataset loads but returns no samples

**Solution 1**: Check label_dict in config
```python
# Ensure labels are correct
config['label_dict'] = {
    'FF-real': 0,
    'FF-DF': 1,
    'FF-F2F': 1,
    # ... all your labels
}
```

**Solution 2**: Verify compression level
```python
# In config
compression: 'c23'  # Must match your dataset folders
```

**Solution 3**: Check train/test split
```python
# Print dataset info
print(f"Train samples: {len(train_dataset)}")
print(f"Test samples: {len(test_dataset)}")
```

---

## Warning Suppression

### Issue: TensorFlow Warnings

**Problem**: TensorFlow CUDA warnings clutter output
```
W tensorflow/compiler/xla/stream_executor/...
```

**Solution**: Suppress at start of script
```python
import os
import warnings

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Suppress Python warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
```

**Why this happens**: Kaggle pre-installs TensorFlow, which loads with CUDA

**Result**: Clean output showing only relevant information

### Issue: TensorBoard Warnings

**Problem**: TensorBoard import errors
```
AttributeError: module 'google.protobuf.descriptor' has no attribute '_internal_create_key'
```

**Solution**: Already fixed in v2.0.0! TensorBoard is now optional.

**Verification**:
```python
# Should work without TensorBoard installed
from deepfakebench.detectors import XceptionDetector
# No errors!
```

**Install TensorBoard if needed**:
```bash
pip install tensorboard
```

### Issue: Deprecation Warnings

**Problem**: NumPy/PyTorch deprecation warnings

**Solution**: Already fixed in v2.0.0! All deprecated APIs updated.

**If you still see warnings**:
```python
# Suppress all warnings
import warnings
warnings.filterwarnings('ignore')

# Or suppress specific warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
```

---

## Optional Dependencies

### Issue: TensorBoard Not Available

**Status**: ✅ **Not an Error** - TensorBoard is optional

**What it means**: Training visualization is disabled but everything else works

**If you need TensorBoard**:
```bash
pip install tensorboard
```

**Usage**:
```python
# Will work if tensorboard is installed
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter('./logs')
```

### Issue: Dlib Not Found

**Status**: ✅ **Not an Error** - Dlib is optional

**What it means**: Face detection for preprocessing unavailable

**When you need dlib**:
- Using FWA blending features
- Running face preprocessing

**Installation**:
```bash
# Ubuntu/Debian
sudo apt-get install cmake
pip install dlib

# macOS
brew install cmake
pip install dlib

# Windows
# Download pre-built wheel from:
# https://github.com/sachadee/Dlib
pip install dlib-19.X.X-cpXX-cpXX-win_amd64.whl
```

### Issue: SlowFast Dependencies

**Problem**: Warning about missing simplejson
```
UserWarning: SlowFast setup skipped: No module named 'simplejson'
```

**Status**: ⚠️ **Minor Issue** - Only affects SlowFast video detector

**Solution**: Install simplejson (only if using SlowFast)
```bash
pip install simplejson
```

**Alternative**: Ignore warning if not using SlowFast detector

### Issue: Missing dlib Model File

**Problem**: Cannot load shape predictor
```
RuntimeError: Unable to open dlib model file
```

**Solution**: Download shape predictor
```bash
# Download shape_predictor_81_face_landmarks.dat
wget https://github.com/SCLBD/DeepfakeBench/releases/download/v1.0.0/shape_predictor_81_face_landmarks.dat

# Move to correct location
mv shape_predictor_81_face_landmarks.dat deepfakebench/preprocessing/dlib_tools/
```

**When you need it**: Only for face preprocessing, not for training/testing

---

## Platform-Specific Issues

### Kaggle-Specific

#### Issue: Kernel Timeout

**Problem**: Kaggle kernel stops after 30 minutes of inactivity

**Solution**: Keep kernel active or save checkpoints frequently
```python
# Save checkpoint every N epochs
if epoch % save_interval == 0:
    torch.save(model.state_dict(), f'/kaggle/working/checkpoint_epoch_{epoch}.pth')
```

#### Issue: File Persistence

**Problem**: Files disappear after kernel restart

**Solution**: Save to /kaggle/working/
```python
# Files here persist
output_dir = '/kaggle/working/outputs'
os.makedirs(output_dir, exist_ok=True)
```

### Windows-Specific

#### Issue: Path Separator Errors

**Problem**: Windows uses backslash (\) in paths

**Solution**: Use pathlib or forward slashes
```python
from pathlib import Path
dataset_path = Path('/kaggle/input/dataset')

# Or use forward slashes (works on Windows)
dataset_path = '/kaggle/input/dataset'
```

#### Issue: Long Path Limit

**Problem**: Windows 260 character path limit

**Solution**: Enable long paths or use shorter paths
```bash
# Enable long paths (requires admin)
# Run in PowerShell as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

## Debugging Tips

### Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or for specific logger
logger = logging.getLogger('deepfakebench')
logger.setLevel(logging.DEBUG)
```

### Check Package Version

```python
import deepfakebench
print(f"Version: {deepfakebench.__version__}")

import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA: {torch.version.cuda}")

import numpy as np
print(f"NumPy: {np.__version__}")
```

### Verify Installation

```python
# Run test script
!python test_local.py
```

### Profile Memory Usage

```python
import psutil
import torch

def print_memory_usage():
    # CPU memory
    process = psutil.Process()
    cpu_mem = process.memory_info().rss / 1e9
    print(f"CPU Memory: {cpu_mem:.2f} GB")
    
    # GPU memory
    if torch.cuda.is_available():
        gpu_mem = torch.cuda.memory_allocated() / 1e9
        gpu_reserved = torch.cuda.memory_reserved() / 1e9
        print(f"GPU Memory: {gpu_mem:.2f} GB allocated, {gpu_reserved:.2f} GB reserved")

print_memory_usage()
```

### Test Import Chain

```python
# Test each level
import deepfakebench
print("✓ Package imported")

from deepfakebench import detectors
print("✓ Detectors module imported")

from deepfakebench.detectors import XceptionDetector
print("✓ XceptionDetector imported")

detector = XceptionDetector({'pretrained': 'None'})
print("✓ Detector instantiated")
```

---

## Getting Help

### Before Opening an Issue

1. **Check existing issues**: Search for similar problems
2. **Try solutions above**: Most common issues are covered
3. **Update to latest version**: Bug may be fixed
4. **Collect information**: Error messages, versions, environment

### Information to Include

When opening an issue, include:

```python
# System information
import sys
import torch
import deepfakebench

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"DeepfakeBench: {deepfakebench.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Error message (full traceback)
# Steps to reproduce
# Expected vs actual behavior
```

### Where to Get Help

- **GitHub Issues**: https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues
- **Documentation**: Check README.md and other guides
- **Stack Overflow**: Tag with `deepfake-detection`

---

## Summary of Fixes in v2.0.0

All these issues are **already fixed** in version 2.0.0:

✅ **NumPy Deprecated Types** - All 34 files updated  
✅ **Import Path Errors** - 73+ files corrected  
✅ **TensorBoard Required** - Made optional (28 files)  
✅ **CUDA Checks** - Lazy loading implemented  
✅ **Dlib Required** - Lazy loading implemented  
✅ **Pretrained Validation** - Path checks added  
✅ **PyTorch Deprecated APIs** - Updated to 2.x  

**Ensure you're using v2.0.0 or later**:
```python
import deepfakebench
assert deepfakebench.__version__ >= "2.0.0"
```

---

**Still having issues?** Open an issue on GitHub with full details!
