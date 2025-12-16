# DeepFakeBench Dataset Guide

Comprehensive guide for downloading, preparing, and adding datasets to DeepFakeBench.

## Table of Contents

- [Supported Datasets](#supported-datasets)
- [Dataset Download](#dataset-download)
- [Dataset Preparation](#dataset-preparation)
- [Dataset Structure](#dataset-structure)
- [Adding Custom Datasets](#adding-custom-datasets)
- [LMDB Conversion](#lmdb-conversion)
- [Configuration](#configuration)

---

## Supported Datasets

DeepFakeBench supports the following benchmark datasets:

| Dataset | Real Videos | Fake Videos | Manipulation Types | Access |
|---------|-------------|-------------|-------------------|--------|
| **FaceForensics++** | 1,000 | 4,000 | DF, F2F, FS, NT | [Request](https://github.com/ondyari/FaceForensics) |
| **CelebDF-v2** | 590 | 5,639 | Face Swap | [Download](https://github.com/yuezunli/celeb-deepfakeforensics) |
| **DFDC** | 23,654 | 104,500 | Multiple | [Download](https://dfdc.ai) |
| **DeeperForensics** | 50,000 | 10,000 | DF-VAE | [Request](https://github.com/EndlessSora/DeeperForensics-1.0) |
| **UADFV** | 49 | 49 | Face Swap | [Download](https://github.com/danmohaha/WIFS2018_In_Ictu_Oculi) |
| **DFD** | 363 | 3,068 | DeepFake | [Download](https://ai.google.com/research/ConEvaluation) |
| **DFDCP** | 1,000 | 2,000 | Multiple | [Request](https://github.com/jasonleenyc/Deep-Fake-Detection) |

---

## Dataset Download

### FaceForensics++

1. **Request Access**: Fill out the [Google Form](https://github.com/ondyari/FaceForensics)

2. **Download Script**:
   ```bash
   # After receiving access
   python scripts/data/download_faceforensics.py \
       --data_path ./datasets/FaceForensics++ \
       --server <provided_server>
   ```

3. **Directory Structure** (after download):
   ```
   datasets/FaceForensics++/
   ├── original_sequences/
   │   └── youtube/
   ├── manipulated_sequences/
   │   ├── Deepfakes/
   │   ├── Face2Face/
   │   ├── FaceSwap/
   │   └── NeuralTextures/
   └── masks/
   ```

### CelebDF-v2

```bash
# Download from official source
wget -P ./datasets/ https://github.com/yuezunli/celeb-deepfakeforensics/releases/download/v2/Celeb-DF-v2.zip

# Extract
unzip ./datasets/Celeb-DF-v2.zip -d ./datasets/
```

### DFDC (Deepfake Detection Challenge)

1. **Register at Kaggle**: [DFDC Competition](https://www.kaggle.com/c/deepfake-detection-challenge)

2. **Download using Kaggle API**:
   ```bash
   kaggle competitions download -c deepfake-detection-challenge -p ./datasets/DFDC/
   ```

---

## Dataset Preparation

### Step 1: Extract Frames

```bash
# Extract frames from videos
python scripts/data/extract_frames.py \
    --input_dir ./datasets/raw_videos \
    --output_dir ./datasets/rgb \
    --fps 10 \
    --max_frames 300
```

### Step 2: Face Extraction

```bash
# Extract and align faces
python deepfakebench/preprocessing/extract_faces.py \
    --input_dir ./datasets/rgb \
    --output_dir ./datasets/faces \
    --detector dlib \
    --align True \
    --size 256
```

### Step 3: Generate Metadata

```bash
# Generate JSON metadata files
python scripts/data/generate_metadata.py \
    --dataset_dir ./datasets/FaceForensics++ \
    --output_dir ./deepfakebench/preprocessing/dataset_json
```

---

## Dataset Structure

### Expected Directory Layout

```
datasets/
├── rgb/                          # Raw frame images
│   ├── FaceForensics++/
│   │   ├── FF-real/
│   │   │   ├── video_001/
│   │   │   │   ├── frame_0001.png
│   │   │   │   ├── frame_0002.png
│   │   │   │   └── ...
│   │   ├── FF-DF/
│   │   ├── FF-F2F/
│   │   ├── FF-FS/
│   │   └── FF-NT/
│   ├── CelebDF/
│   │   ├── CelebDFv2_real/
│   │   └── CelebDFv2_fake/
│   └── ...
│
├── lmdb/                         # LMDB format (faster loading)
│   ├── FaceForensics++/
│   └── ...
│
└── landmarks/                    # Facial landmarks (optional)
    └── ...
```

### Metadata JSON Format

Located in `deepfakebench/preprocessing/dataset_json/`:

```json
{
  "FaceForensics++": {
    "FF-real": {
      "video_001": {
        "label": 0,
        "frames": ["frame_0001.png", "frame_0002.png", "..."],
        "num_frames": 300,
        "path": "FaceForensics++/FF-real/video_001"
      }
    },
    "FF-DF": {
      "video_001": {
        "label": 1,
        "frames": ["..."],
        "num_frames": 300,
        "path": "FaceForensics++/FF-DF/video_001"
      }
    }
  }
}
```

---

## Adding Custom Datasets

### Step 1: Prepare Directory Structure

```bash
mkdir -p datasets/rgb/MyDataset/MyDataset_real
mkdir -p datasets/rgb/MyDataset/MyDataset_fake
```

### Step 2: Create Dataset Configuration

Create `deepfakebench/preprocessing/dataset_json/mydataset.json`:

```json
{
  "MyDataset": {
    "MyDataset_real": {
      "video_001": {
        "label": 0,
        "frames": ["frame_0001.png", "frame_0002.png"],
        "num_frames": 100,
        "path": "MyDataset/MyDataset_real/video_001"
      }
    },
    "MyDataset_fake": {
      "video_001": {
        "label": 1,
        "frames": ["frame_0001.png", "frame_0002.png"],
        "num_frames": 100,
        "path": "MyDataset/MyDataset_fake/video_001"
      }
    }
  }
}
```

### Step 3: Update Label Dictionary

Add to `deepfakebench/config/train_config.yaml`:

```yaml
label_dict:
  # ... existing labels ...
  # Add your dataset labels
  MyDataset_real: 0
  MyDataset_fake: 1
```

### Step 4: Register Dataset (Optional)

For custom dataset classes, create `deepfakebench/dataset/my_dataset.py`:

```python
"""Custom Dataset Implementation"""

from .abstract_dataset import DeepfakeAbstractBaseDataset


class MyDataset(DeepfakeAbstractBaseDataset):
    """Custom dataset for MyDataset."""
    
    def __init__(self, config, mode='train'):
        super().__init__(config, mode)
        # Custom initialization
    
    def __getitem__(self, index):
        # Custom data loading logic
        return super().__getitem__(index)
    
    def collate_fn(self, batch):
        # Custom batch collation
        return super().collate_fn(batch)
```

Register in `deepfakebench/dataset/__init__.py`:

```python
from .my_dataset import MyDataset
```

---

## LMDB Conversion

Convert datasets to LMDB format for faster data loading:

```bash
# Convert single dataset
python scripts/data/convert_to_lmdb.py \
    --input_dir ./datasets/rgb/FaceForensics++ \
    --output_dir ./datasets/lmdb/FaceForensics++ \
    --num_workers 8

# Convert all datasets
python scripts/data/convert_all_to_lmdb.py \
    --rgb_dir ./datasets/rgb \
    --lmdb_dir ./datasets/lmdb \
    --num_workers 8
```

### LMDB Configuration

Enable LMDB in training config:

```yaml
# train_config.yaml
lmdb: True
lmdb_dir: ./datasets/lmdb
```

---

## Configuration

### Environment Variables

```bash
# Set dataset paths via environment variables
export DEEPFAKEBENCH_DATASETS_DIR=/path/to/datasets
export DEEPFAKEBENCH_RGB_DIR=/path/to/datasets/rgb
export DEEPFAKEBENCH_LMDB_DIR=/path/to/datasets/lmdb
```

### Configuration Files

#### Local Configuration (`config/local_config.yaml`)

```yaml
paths:
  datasets: ./datasets
  rgb_dir: ./datasets/rgb
  lmdb_dir: ./datasets/lmdb
```

#### Training Configuration

```yaml
# deepfakebench/config/train_config.yaml
rgb_dir: './datasets/rgb'
lmdb_dir: './datasets/lmdb'
dataset_json_folder: './deepfakebench/preprocessing/dataset_json'
```

---

## Data Augmentation

### Available Augmentations

```yaml
# In detector config
augmentations:
  - type: HorizontalFlip
    p: 0.5
  - type: RandomBrightnessContrast
    p: 0.3
  - type: GaussianNoise
    p: 0.2
  - type: ImageCompression
    quality_lower: 60
    quality_upper: 100
    p: 0.3
```

### Custom Augmentation Pipeline

See `deepfakebench/dataset/albu.py` for augmentation implementations.

---

## Verification

### Verify Dataset Structure

```bash
python scripts/data/verify_dataset.py \
    --dataset_dir ./datasets/rgb/FaceForensics++ \
    --check_frames \
    --check_labels
```

### Test Data Loading

```python
from deepfakebench.config import get_config
from deepfakebench.dataset import DeepfakeAbstractBaseDataset

# Load config
config = get_config("config/train_config.yaml")

# Create dataset
dataset = DeepfakeAbstractBaseDataset(config, mode='train')

# Test loading
sample = dataset[0]
print(f"Image shape: {sample['image'].shape}")
print(f"Label: {sample['label']}")
```

---

## Common Issues

### Issue: "Dataset not found"

**Solution**: Check paths in configuration files match actual directories.

### Issue: "Label mismatch"

**Solution**: Ensure `label_dict` in config includes all dataset labels.

### Issue: "Corrupt images"

**Solution**: Run verification script and re-extract corrupt frames.

---

## Next Steps

- [Model Guide](MODEL_GUIDE.md) - Download pretrained models
- [Training Guide](TRAINING_GUIDE.md) - Train detection models
- [Detection Guide](DETECTION_GUIDE.md) - Run inference
