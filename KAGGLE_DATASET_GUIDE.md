# Kaggle Dataset Structure Guide

## ✅ Your Dataset Structure is Fully Compatible!

The DeepfakeBench system **already supports** your Kaggle dataset structure without any modifications needed.

## Your Kaggle Dataset Structure

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

## How the System Works

### 1. Dataset JSON Preprocessing

The system uses JSON files to map video paths. The `preprocessing/rearrange.py` script handles the exact structure you have:

**For Real Videos:**
```python
# Scans: original_sequences/youtube/c23/frames/
# Creates mapping: FaceForensics++/FF-real/train|test/c23/{video_name}
```

**For Fake Videos:**
```python
# Scans: manipulated_sequences/{method}/c23/frames/
# Creates mapping: FaceForensics++/FF-{method}/train|test/c23/{video_name}
```

### 2. Supported Methods in Your Dataset

| Folder Name | System Label | Description |
|-------------|--------------|-------------|
| Face2Face | FF-F2F | Face reenactment |
| Deepfakes | FF-DF | Face swap |
| FaceSwap | FF-FS | Face swap |
| NeuralTextures | FF-NT | Face reenactment |
| FaceShifter | FF-FH | Face swap |
| DeepFakeDetection | FF-DFD | Mixed methods |
| youtube (original) | FF-real | Real videos |

### 3. Compression Levels

Your dataset uses **c23** (compression level 23). The system supports:
- `c23` - Standard compression (your dataset)
- `c40` - Higher compression
- `raw` - Uncompressed

## Configuration for Kaggle

### Step 1: Generate Dataset JSON

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

This will create: `deepfakebench/preprocessing/dataset_json/FaceForensics++.json`

### Step 2: Update Configuration

```python
import yaml

# Load config
with open('deepfakebench/config/detector/sladd_detector.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Update paths for Kaggle
config['rgb_dir'] = '/kaggle/input/faceforensicsplusplus-c23-deepfakebench-structure/rgb'
config['dataset_json_folder'] = './preprocessing/dataset_json'
config['compression'] = 'c23'  # Your compression level
config['train_dataset'] = ['FaceForensics++']  # or specific methods: ['FF-F2F', 'FF-DF']
config['test_dataset'] = 'FaceForensics++'

# Save modified config
with open('kaggle_config.yaml', 'w') as f:
    yaml.dump(config, f)
```

### Step 3: Train or Test

```python
from deepfakebench.train import train
from deepfakebench.test import test

# Training
train(config='kaggle_config.yaml')

# Or Testing
test(config='kaggle_config.yaml', ckpt_path='path/to/checkpoint.pth')
```

## Quick Test Script for Kaggle

```python
# Test if your dataset structure is readable
import os

base_path = '/kaggle/input/faceforensicsplusplus-c23-deepfakebench-structure/rgb/FaceForensics++'

# Check structure
print("✓ Checking dataset structure...")

# Check manipulated sequences
manip_path = os.path.join(base_path, 'manipulated_sequences')
if os.path.exists(manip_path):
    methods = os.listdir(manip_path)
    print(f"✓ Found {len(methods)} manipulation methods: {methods}")
    
    for method in methods:
        c23_frames = os.path.join(manip_path, method, 'c23', 'frames')
        if os.path.exists(c23_frames):
            videos = os.listdir(c23_frames)
            print(f"  - {method}: {len(videos)} videos")

# Check original sequences
orig_path = os.path.join(base_path, 'original_sequences', 'youtube', 'c23', 'frames')
if os.path.exists(orig_path):
    videos = os.listdir(orig_path)
    print(f"✓ Found {len(videos)} original (real) videos")

print("\n✅ Your dataset structure is correct!")
```

## Dataset Statistics

Run this to get detailed statistics:

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

## Training on Specific Methods

You can train on specific manipulation methods:

```python
# Train only on Deepfakes
config['train_dataset'] = ['FF-DF']

# Train on multiple methods
config['train_dataset'] = ['FF-F2F', 'FF-DF', 'FF-FS']

# Train on all (FaceForensics++ includes all)
config['train_dataset'] = ['FaceForensics++']
```

## Cross-Dataset Testing

```python
# Train on one, test on another
config['train_dataset'] = ['FF-F2F']
config['test_dataset'] = 'FF-DF'  # Test generalization
```

## Notes

1. **Automatic Detection**: The `rearrange.py` script automatically detects your folder structure
2. **Compression Handling**: System reads from `c23` folder as specified in your structure
3. **Frame Extraction**: System expects frames already extracted (which yours are)
4. **Masks**: Optional - if masks exist in `manipulated_sequences/{method}/c23/masks/`, they'll be loaded
5. **Video Names**: Must be valid folder names under the `frames/` directory

## Troubleshooting

**Q: JSON generation fails**
- Check that `frames/` subdirectories exist under each compression level
- Verify video folders contain actual frame images (.png, .jpg)

**Q: "Dataset not found" error**
- Ensure `dataset_json_folder` points to where JSON was generated
- Check that JSON file name matches dataset name in config

**Q: Empty dataset**
- Verify `compression` in config matches your folder structure (c23)
- Check `label_dict` in config includes all your labels

**Q: Performance issues**
- Consider using LMDB format for faster loading (see LMDB section below)

## LMDB Conversion (Optional - For Speed)

For faster loading, convert to LMDB format:

```python
from deepfakebench.preprocessing.dataset2lmdb import convert_to_lmdb

convert_to_lmdb(
    json_path='./preprocessing/dataset_json/FaceForensics++.json',
    output_path='/kaggle/working/lmdb',
    compression='c23'
)

# Update config
config['lmdb'] = True
config['lmdb_dir'] = '/kaggle/working/lmdb'
```

## ✅ Summary

Your dataset structure is **100% compatible** with DeepfakeBench. No reorganization needed! The system will:
1. Scan your `manipulated_sequences` and `original_sequences` folders
2. Map videos to train/test splits
3. Load frames from the `c23/frames/` directories
4. Apply the correct labels automatically
