# 🚀 DeepfakeBench on Kaggle

Complete guide to running DeepfakeBench on Kaggle notebooks with GPU support.

## Quick Start (2 Minutes Setup)

### Method 1: One-Line Clone & Install

```bash
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
!bash install.sh
```

### Method 2: Manual Step-by-Step

**Step 1: Clone Repository**
```bash
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
```

**Step 2: Quick Install (Core Packages Only)**
```bash
# Install PyTorch (usually pre-installed on Kaggle)
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install essential packages
!pip install opencv-python==4.6.0.66 scikit-image scikit-learn albumentations
!pip install efficientnet-pytorch timm tensorboard
!pip install transformers --no-deps
!pip install tokenizers regex
```

**Step 3: Verify Installation**
```python
import torch
import sys
sys.path.insert(0, 'training')

print(f"✓ PyTorch: {torch.__version__}")
print(f"✓ CUDA Available: {torch.cuda.is_available()}")
print(f"✓ GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")

# Test import
from detectors.xception_detector import XceptionDetector
print("✓ DeepfakeBench imported successfully!")
```

## Dataset Setup on Kaggle

### Option 1: Use Kaggle Datasets

Add datasets from Kaggle:
1. Go to notebook settings → Add Data
2. Search for: "FaceForensics++", "Celeb-DF", or "DFDC"
3. Add to notebook

```python
# Link Kaggle dataset to DeepfakeBench structure
!mkdir -p datasets/rgb
!ln -s /kaggle/input/faceforensics datasets/rgb/FaceForensics++
```

### Option 2: Download from Google Drive

```bash
# Install gdown
!pip install gdown

# Download datasets (replace FILE_ID with actual Google Drive file ID)
!gdown --id FILE_ID -O datasets.zip
!unzip datasets.zip -d datasets/
```

## Training on Kaggle

### Quick Training Example

```python
# Set GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Run training
!python training/train.py \
    --detector_path ./training/config/detector/xception.yaml \
    --train_dataset FaceForensics++ \
    --test_dataset Celeb-DF
```

### Configuration

Edit detector config files in `training/config/detector/`:
- Adjust `batch_size` based on GPU memory (Kaggle P100: 16-32)
- Set `num_epochs` appropriately
- Configure data paths

## Example Kaggle Notebook Structure

```python
# Cell 1: Clone & Install
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
!bash install.sh

# Cell 2: Setup Data
!mkdir -p datasets/rgb
!ln -s /kaggle/input/your-dataset datasets/rgb/FaceForensics++

# Cell 3: Import & Verify
import torch
import sys
sys.path.insert(0, 'training')
from detectors.xception_detector import XceptionDetector

print(f"✓ GPU: {torch.cuda.get_device_name(0)}")

# Cell 4: Train
!python training/train.py \
    --detector_path ./training/config/detector/xception.yaml

# Cell 5: Evaluate
!python training/test.py \
    --detector_path ./training/config/detector/xception.yaml \
    --weights_path path/to/checkpoint.pth
```

## Kaggle-Specific Tips

### GPU Memory Optimization
```python
# Reduce batch size in config
batch_size: 16  # for P100 (16GB)
batch_size: 8   # for T4 (16GB)
batch_size: 4   # if OOM errors occur
```

### Save Outputs to Kaggle
```python
# Save checkpoints to /kaggle/working/ (persists after kernel stops)
import shutil
shutil.copy('output/checkpoint.pth', '/kaggle/working/')
```

### Time Limits
- Kaggle free tier: 30 hours/week GPU
- Enable "Save Version" to preserve progress
- Use checkpoint resuming for long training

## Troubleshooting

### Import Errors
```python
# Add training folder to path
import sys
sys.path.insert(0, 'training')
```

### CUDA Out of Memory
- Reduce `batch_size` in detector config
- Use gradient accumulation
- Enable mixed precision training

### Dataset Path Issues
```python
# Check if dataset is mounted
!ls /kaggle/input/
!ls datasets/rgb/
```

## Pre-trained Weights on Kaggle

```bash
# Download from GitHub releases
!wget https://github.com/SCLBD/DeepfakeBench/releases/download/v1.0.1/xception.pth \
    -O training/pretrained/xception.pth
```

## Full Kaggle Notebook Example

See our example notebook: [DeepfakeBench Kaggle Demo](https://www.kaggle.com/code/your-username/deepfakebench-demo)

## Performance Benchmarks on Kaggle

| GPU Type | Batch Size | Training Speed | Memory Usage |
|----------|-----------|----------------|--------------|
| P100     | 32        | ~120 samples/s | 14GB         |
| T4       | 16        | ~80 samples/s  | 12GB         |
| TPU      | N/A       | Not supported  | N/A          |

## Support

- Issues: [GitHub Issues](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues)
- Original Repo: [SCLBD/DeepfakeBench](https://github.com/SCLBD/DeepfakeBench)

---

**Note:** This upgraded version includes:
- ✅ PyTorch 2.x compatibility
- ✅ Python 3.8+ support
- ✅ Secure model loading
- ✅ Modern API usage
