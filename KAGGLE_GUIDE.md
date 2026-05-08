# 🚀 Complete Kaggle Guide for DeepFakeBench

> **Quick Setup**: Get started in 2-3 minutes on Kaggle with GPU support

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Setup & Installation](#-setup--installation)
- [Testing](#-testing)
- [Dataset Configuration](#-dataset-configuration)
- [Troubleshooting](#-troubleshooting)
- [Technical Details](#-technical-details)

---

## 🎯 Quick Start

### Prerequisites

> **⚠️ IMPORTANT:** Enable GPU in your Kaggle notebook first!
> - Go to notebook Settings (right panel)
> - Accelerator → Select **GPU T4 x2** or **P100**
> - Click **Save**

### 2-Minute Setup

Run these cells in order:

**Cell 1: Clone Repository**
```python
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
```

**Cell 2: Install Dependencies**
```python
!bash kaggle_install.sh
```

**Cell 3: Test Import**
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

**Cell 4: Create Detector**
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
    'typeloss_func': 'am_softmax',
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
        features = features[0]
print(f"✓ Feature extraction successful, output shape: {features.shape}")
```

### Expected Output

```
✓ Package version: 2.0.0
✓ Successfully imported SLADDXceptionDetector
Creating detector...
✓ Detector created successfully
✓ Device: cpu
✓ Model has 20.83M parameters
✓ Feature extraction successful, output shape: torch.Size([1, 2048, 8, 8])
```

---

## 💻 Setup & Installation

### Method 1: Automated Installation (Recommended)

```bash
# Clone and install in one go
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
!bash kaggle_install.sh
```

**Installation Time**: 2-3 minutes  
**What Gets Installed**:
- Core dependencies (PyTorch, OpenCV, etc.)
- Image processing libraries
- Dataset utilities
- Optional packages

### Method 2: Manual Installation

```bash
# Step 1: Clone
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded

# Step 2: Install core packages
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Step 3: Install dependencies
!pip install opencv-python==4.6.0.66 scikit-image scikit-learn albumentations
!pip install efficientnet-pytorch timm tensorboard
!pip install transformers --no-deps
!pip install tokenizers regex
```

### Environment Verification

```python
import torch
import sys
sys.path.insert(0, '/kaggle/working/DeepFakeBenchUpgraded')

print(f"✓ PyTorch: {torch.__version__}")
print(f"✓ CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("⚠️ GPU not detected - Enable in Settings → Accelerator → GPU T4 x2")
```

---

## 🧪 Testing

### Basic Import Test

```python
import sys
sys.path.insert(0, '/kaggle/working/DeepFakeBenchUpgraded')

from deepfakebench.detectors.sladd_detector import SLADDXceptionDetector
print("✓ DeepfakeBench imported successfully!")
```

### Load Configuration from YAML

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

### Test with Multiple Detectors

```python
from deepfakebench.detectors.xception_detector import XceptionDetector
from deepfakebench.detectors.efficientnetb4_detector import EfficientNetB4Detector
from deepfakebench.detectors.sladd_detector import SLADDXceptionDetector

detectors = {
    'Xception': XceptionDetector,
    'EfficientNet-B4': EfficientNetB4Detector,
    'SLADD-Xception': SLADDXceptionDetector
}

for name, detector_class in detectors.items():
    try:
        # Create minimal config
        config = {'pretrained': 'None', 'backbone_name': name.lower().replace('-', '_')}
        detector = detector_class(config)
        print(f"✓ {name}: Successfully loaded")
    except Exception as e:
        print(f"✗ {name}: Failed - {str(e)}")
```

---

## 📊 Dataset Configuration

### Supported Dataset Structure

Your Kaggle dataset is fully compatible! The system supports this exact structure:

```
/kaggle/input/faceforensicsplusplus-c23-deepfakebench-structure/
└── rgb/
    └── FaceForensics++/
        ├── manipulated_sequences/
        │   ├── Face2Face/
        │   │   └── c23/
        │   │       ├── frames/
        │   │       │   └── [video_name_folders]/
        │   │       │       └── [frame_files.png]
        │   │       └── masks/ (optional)
        │   ├── Deepfakes/
        │   ├── DeepFakeDetection/
        │   ├── NeuralTextures/
        │   ├── FaceShifter/
        │   └── FaceSwap/
        └── original_sequences/
            └── youtube/
                └── c23/
                    └── frames/
                        └── [video_name_folders]/
                            └── [frame_files.png]
```

### Dataset Setup on Kaggle

#### Option 1: Use Kaggle Datasets

1. Go to notebook settings → Add Data
2. Search for: "FaceForensics++", "Celeb-DF", or "DFDC"
3. Add to notebook

```python
# Link Kaggle dataset to DeepfakeBench structure
!mkdir -p datasets/rgb
!ln -s /kaggle/input/faceforensics datasets/rgb/FaceForensics++
```

#### Option 2: Configure Existing Dataset

```python
import os
import yaml

# Check if dataset is mounted
dataset_path = '/kaggle/input/faceforensicsplusplus-c23-deepfakebench-structure/rgb/FaceForensics++'
print(f"Dataset exists: {os.path.exists(dataset_path)}")

# List manipulation methods
manip_path = os.path.join(dataset_path, 'manipulated_sequences')
if os.path.exists(manip_path):
    methods = os.listdir(manip_path)
    print(f"Found {len(methods)} manipulation methods: {methods}")
```

### Generate Dataset JSON

```python
import sys
sys.path.insert(0, '/kaggle/working/DeepFakeBenchUpgraded')

from deepfakebench.preprocessing.rearrange import generate_dataset_file
import os

# Create output directory
os.makedirs('./deepfakebench/preprocessing/dataset_json', exist_ok=True)

# Generate JSON mapping for your dataset
generate_dataset_file(
    dataset_name='FaceForensics++',
    dataset_root_path='/kaggle/input/faceforensicsplusplus-c23-deepfakebench-structure/rgb/FaceForensics++',
    output_file_path='./deepfakebench/preprocessing/dataset_json/FaceForensics++.json',
    compression_level='c23'
)
```

### Dataset Statistics

```python
import os
from collections import defaultdict

base_path = '/kaggle/input/faceforensicsplusplus-c23-deepfakebench-structure/rgb/FaceForensics++'

stats = defaultdict(lambda: {'videos': 0, 'frames': 0})

# Count manipulated
manip_path = os.path.join(base_path, 'manipulated_sequences')
for method in os.listdir(manip_path):
    frames_path = os.path.join(manip_path, method, 'c23', 'frames')
    if os.path.exists(frames_path):
        videos = os.listdir(frames_path)
        stats[method]['videos'] = len(videos)
        
        # Count frames in first video (sample)
        if videos:
            first_video = os.path.join(frames_path, videos[0])
            frames = len(os.listdir(first_video))
            stats[method]['frames'] = frames

# Count original
orig_path = os.path.join(base_path, 'original_sequences', 'youtube', 'c23', 'frames')
videos = os.listdir(orig_path)
stats['youtube (real)']['videos'] = len(videos)
if videos:
    first_video = os.path.join(orig_path, videos[0])
    frames = len(os.listdir(first_video))
    stats['youtube (real)']['frames'] = frames

# Print report
print("Dataset Statistics:")
print("=" * 60)
for method, data in stats.items():
    print(f"{method:20s}: {data['videos']:4d} videos, ~{data['frames']:3d} frames/video")
print("=" * 60)
total_videos = sum(s['videos'] for s in stats.values())
print(f"Total: {total_videos} videos")
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: `ModuleNotFoundError`

**Problem**: Cannot import deepfakebench modules
```python
ModuleNotFoundError: No module named 'deepfakebench'
```

**Solution**: Add package to Python path
```python
import sys
sys.path.insert(0, '/kaggle/working/DeepFakeBenchUpgraded')
# Now imports will work
from deepfakebench.detectors import XceptionDetector
```

#### Issue: GPU Not Detected

**Problem**: CUDA not available
```python
print(torch.cuda.is_available())  # Returns False
```

**Solution**: Enable GPU in notebook settings
1. Go to Settings (right panel)
2. Accelerator → Select **GPU T4 x2** or **P100**
3. Click **Save**
4. Restart kernel

#### Issue: Out of Memory (OOM)

**Problem**: CUDA out of memory error

**Solution**: Reduce batch size in config
```python
# In detector config YAML
batch_size: 16  # for P100 (16GB)
batch_size: 8   # for T4 (16GB)
batch_size: 4   # if OOM errors persist
```

#### Issue: Import Warnings

**Problem**: TensorFlow/TensorBoard warnings cluttering output

**Solution**: Suppress warnings (add at start of notebook)
```python
import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
```

#### Issue: Dataset Path Not Found

**Problem**: Dataset not found error

**Solution**: Verify dataset path
```python
# Check if dataset is mounted
import os
dataset_path = '/kaggle/input/your-dataset-name'
print(f"Dataset exists: {os.path.exists(dataset_path)}")
print(f"Contents: {os.listdir(dataset_path)}")
```

#### Issue: SlowFast Dependencies Warning

**Problem**: Warning about missing simplejson

**Solution**: Install simplejson (only if using SlowFast detector)
```bash
!pip install simplejson
```

---

## 📖 Technical Details

### What Gets Installed

The `kaggle_install.sh` script installs:

1. **Core Dependencies**
   - lmdb (database for fast data loading)
   - scikit-learn (evaluation metrics)
   - pyyaml (config parsing)

2. **Image Processing**
   - opencv-python (computer vision)
   - scikit-image (image processing)
   - albumentations (augmentation)
   - imgaug (augmentation)

3. **Deep Learning**
   - efficientnet-pytorch (EfficientNet models)
   - timm (model library)
   - transformers (CLIP-based models)

4. **Optional** (commented by default)
   - tensorboard (training visualization)
   - dlib (face detection for preprocessing)

### Installation Process

The script uses `--no-deps` flags to avoid version conflicts with Kaggle's pre-installed packages:

```bash
pip install -q --no-deps opencv-python
pip install -q --no-deps albumentations
pip install -q --no-deps imgaug
```

### Performance Benchmarks

| Metric | Value |
|--------|-------|
| Installation Time | 2-3 minutes |
| Import Time | <5 seconds |
| Model Load Time | ~2 seconds |
| Inference (1 image) | ~50ms (GPU) |
| Memory Usage | ~2GB GPU |

### Kaggle GPU Specifications

| GPU Type | Memory | CUDA | PyTorch Support |
|----------|--------|------|----------------|
| Tesla T4 x2 | 16GB | 12.4 | ✅ 2.x |
| Tesla P100 | 16GB | 12.4 | ✅ 2.x |

### Known Limitations

1. **Pretrained Weights Not Included**
   - Must download separately from releases
   - Can train from scratch using `'None'`

2. **Dataset Must Be Pre-processed**
   - Frames must be extracted
   - Proper folder structure required

3. **Time Limits**
   - Kaggle free tier: 30 hours/week GPU
   - Use checkpoint resuming for long training

### Files Modified for Kaggle Compatibility

- **73+ import paths** fixed with `deepfakebench.` prefix
- **28 files** with optional TensorBoard imports
- **3 files** with lazy loading (dlib, CUDA)
- **34 files** with NumPy/PyTorch compatibility fixes

---

## 🎓 Training on Kaggle

### Quick Training Example

```python
# Set GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Run training
!python deepfakebench/train.py \
    --detector_path ./deepfakebench/config/detector/xception.yaml \
    --train_dataset FaceForensics++ \
    --test_dataset Celeb-DF
```

### Save Outputs

```python
# Save checkpoints to /kaggle/working/ (persists after kernel stops)
import shutil
shutil.copy('output/checkpoint.pth', '/kaggle/working/')
```

---

## 📚 Additional Resources

### Documentation
- **[README.md](README.md)** - Main project documentation
- **[UPDATES.md](UPDATES.md)** - Complete v2.0 changelog
- **[KAGGLE_DATASET_GUIDE.md](KAGGLE_DATASET_GUIDE.md)** - Detailed dataset structure guide
- **[FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md)** - Project organization

### Links
- **Repository**: https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded
- **Original Repo**: https://github.com/SCLBD/DeepfakeBench
- **Paper**: https://arxiv.org/abs/2307.01426

### Support
- **Issues**: [GitHub Issues](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues)
- **Discussions**: Check existing issues first

---

## ✅ Summary

### What Works on Kaggle
- ✅ 2-3 minute installation
- ✅ 36+ detector models
- ✅ GPU T4 and P100 support
- ✅ FaceForensics++ dataset compatibility
- ✅ All imports working correctly
- ✅ Optional TensorBoard support

### Quick Checklist
- [ ] Enable GPU in notebook settings
- [ ] Clone repository
- [ ] Run `kaggle_install.sh`
- [ ] Test imports
- [ ] Create detector instance
- [ ] Load your dataset (optional)
- [ ] Start training/testing

**You're now ready to use DeepFakeBench on Kaggle! 🎉**
