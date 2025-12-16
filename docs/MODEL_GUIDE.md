# DeepFakeBench Model Guide

Guide for downloading pretrained models, adding custom models, and managing model weights.

## Table of Contents

- [Available Models](#available-models)
- [Downloading Pretrained Models](#downloading-pretrained-models)
- [Model Architecture](#model-architecture)
- [Adding Custom Models](#adding-custom-models)
- [Model Registry](#model-registry)
- [Model Configuration](#model-configuration)

---

## Available Models

### CNN-Based Detectors

| Model | Backbone | AUC (FF++) | Parameters | Speed |
|-------|----------|------------|------------|-------|
| **ResNet34** | ResNet-34 | 95.2% | 21.8M | Fast |
| **EfficientNet-B4** | EfficientNet | 97.1% | 19.3M | Medium |
| **Xception** | Xception | 96.5% | 22.9M | Medium |
| **Meso4** | Custom CNN | 84.7% | 0.3M | Very Fast |
| **MesoInception4** | Inception-like | 86.2% | 0.5M | Very Fast |

### Transformer-Based Detectors

| Model | Backbone | AUC (FF++) | Parameters | Speed |
|-------|----------|------------|------------|-------|
| **CLIP** | ViT-B/32 | 93.8% | 428M | Slow |
| **X-CLIP** | X-CLIP | 94.2% | 435M | Slow |
| **TimeSformer** | TimeSformer | 95.1% | 121M | Slow |
| **VideoMAE** | VideoMAE | 94.8% | 86M | Medium |

### Specialized Detectors

| Model | Method | AUC (FF++) | Highlights |
|-------|--------|------------|------------|
| **F3Net** | Frequency Analysis | 96.3% | Frequency domain features |
| **Face X-Ray** | Blending Detection | 95.8% | Detects blending boundaries |
| **SBI** | Self-Blended Images | 94.5% | Self-supervised |
| **SPSL** | Spatial-Phase | 96.1% | Phase spectrum analysis |
| **RECCE** | Reconstruction | 95.9% | Reconstruction error |
| **Multi-Attention** | Attention | 97.2% | Multi-scale attention |
| **UCF** | Universal | 95.4% | Cross-dataset |
| **FWA** | Face Warping | 94.1% | Warping artifacts |

---

## Downloading Pretrained Models

### Automatic Download

```bash
# Download all pretrained models
python scripts/models/download_pretrained.py --all

# Download specific model
python scripts/models/download_pretrained.py --model resnet34

# Download multiple models
python scripts/models/download_pretrained.py --model resnet34 efficientnetb4 xception
```

### Manual Download

Pretrained weights are available at:
- **Google Drive**: [Link](https://drive.google.com/drive/folders/xxx)
- **Hugging Face**: [Link](https://huggingface.co/deepfakebench)

Place downloaded weights in:
```
deepfakebench/pretrained/
├── resnet34_ff++.pth
├── efficientnetb4_ff++.pth
├── xception_ff++.pth
└── ...
```

### Verify Downloads

```python
import torch

# Load and verify checkpoint
checkpoint = torch.load('deepfakebench/pretrained/resnet34_ff++.pth', 
                        map_location='cpu', weights_only=True)
print(f"Model keys: {checkpoint.keys()}")
print(f"Epoch: {checkpoint.get('epoch', 'N/A')}")
print(f"AUC: {checkpoint.get('best_metric', 'N/A')}")
```

---

## Model Architecture

### Base Detector Structure

All detectors inherit from `BaseDetector`:

```python
class BaseDetector(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.backbone = self.build_backbone()
        self.head = self.build_head()
    
    def build_backbone(self):
        """Build feature extraction backbone."""
        raise NotImplementedError
    
    def build_head(self):
        """Build classification head."""
        raise NotImplementedError
    
    def forward(self, x, inference=False):
        """Forward pass."""
        features = self.backbone(x)
        output = self.head(features)
        return output
```

### Network Components

```
deepfakebench/networks/
├── resnet34.py          # ResNet backbone
├── efficientnetb4.py    # EfficientNet backbone
├── xception.py          # Xception backbone
├── mesonet.py           # Meso4/MesoInception
├── vgg.py               # VGG backbone
└── time_transformer.py  # Temporal transformer
```

---

## Adding Custom Models

### Step 1: Create Detector File

Create `deepfakebench/detectors/my_detector.py`:

```python
"""
Custom Detector Implementation
==============================

Author: Your Name
Date: YYYY-MM-DD
Description: Brief description of your detector
"""

import torch
import torch.nn as nn
from .base_detector import AbstractDetector
from deepfakebench.metrics.registry import DETECTOR


@DETECTOR.register_module(module_name='my_detector')
class MyDetector(AbstractDetector):
    """
    My Custom Deepfake Detector.
    
    Args:
        config (dict): Configuration dictionary
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Get parameters from config
        self.num_classes = config.get('num_classes', 2)
        self.backbone_name = config.get('backbone', 'resnet34')
        
        # Build network
        self.backbone = self._build_backbone()
        self.classifier = self._build_classifier()
        
        # Loss function
        self.loss_fn = nn.CrossEntropyLoss()
    
    def _build_backbone(self):
        """Build the feature extraction backbone."""
        if self.backbone_name == 'resnet34':
            from torchvision.models import resnet34, ResNet34_Weights
            backbone = resnet34(weights=ResNet34_Weights.DEFAULT)
            # Remove final FC layer
            backbone.fc = nn.Identity()
            return backbone
        else:
            raise ValueError(f"Unknown backbone: {self.backbone_name}")
    
    def _build_classifier(self):
        """Build the classification head."""
        return nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, self.num_classes)
        )
    
    def forward(self, data_dict: dict, inference: bool = False) -> dict:
        """
        Forward pass.
        
        Args:
            data_dict: Dictionary containing 'image' and optionally 'label'
            inference: Whether in inference mode
            
        Returns:
            Dictionary containing 'cls' (logits), 'prob' (probabilities),
            and 'feat' (features)
        """
        # Extract input
        x = data_dict['image']  # Shape: (B, C, H, W)
        
        # Forward through backbone
        features = self.backbone(x)  # Shape: (B, 512)
        
        # Forward through classifier
        logits = self.classifier(features)  # Shape: (B, num_classes)
        
        # Calculate probabilities
        prob = torch.softmax(logits, dim=1)[:, 1]  # Probability of fake
        
        return {
            'cls': logits,
            'prob': prob,
            'feat': features
        }
    
    def get_losses(self, data_dict: dict, pred_dict: dict) -> dict:
        """
        Calculate losses.
        
        Args:
            data_dict: Input data dictionary
            pred_dict: Prediction dictionary from forward()
            
        Returns:
            Dictionary of losses
        """
        # Get labels
        label = data_dict['label']
        
        # Classification loss
        cls_loss = self.loss_fn(pred_dict['cls'], label)
        
        return {
            'overall': cls_loss,
            'cls': cls_loss
        }
    
    def get_train_metrics(self, data_dict: dict, pred_dict: dict) -> dict:
        """Calculate training metrics."""
        label = data_dict['label']
        pred = pred_dict['prob'] > 0.5
        
        acc = (pred == label).float().mean()
        
        return {'acc': acc.item()}
```

### Step 2: Register Detector

Add import to `deepfakebench/detectors/__init__.py`:

```python
from .my_detector import MyDetector
```

### Step 3: Create Configuration

Create `deepfakebench/config/detector/my_detector.yaml`:

```yaml
# My Detector Configuration
# =========================

# Model settings
model_name: my_detector
backbone: resnet34
num_classes: 2
pretrained: True

# Input settings
resolution: 256
with_mask: False
with_landmark: False

# Training settings
train_batchSize: 32
test_batchSize: 64
lr: 0.0002
weight_decay: 0.0001
nEpochs: 50

# Optimizer
optimizer:
  type: Adam
  betas: [0.9, 0.999]

# Scheduler
scheduler:
  type: CosineAnnealingLR
  T_max: 50
  eta_min: 0.00001

# Data augmentation
augment:
  flip_prob: 0.5
  brightness: 0.2
  contrast: 0.2

# Dataset
frame_num:
  train: 8
  test: 32

# Loss weights
loss_weights:
  cls: 1.0

# Metrics
metric_scoring: auc
```

### Step 4: Test Your Model

```python
import torch
from deepfakebench.detectors import MyDetector

# Create config
config = {
    'model_name': 'my_detector',
    'backbone': 'resnet34',
    'num_classes': 2,
    'resolution': 256
}

# Initialize model
model = MyDetector(config)

# Test forward pass
batch = {
    'image': torch.randn(4, 3, 256, 256),
    'label': torch.tensor([0, 1, 0, 1])
}

output = model(batch)
print(f"Output shape: {output['cls'].shape}")
print(f"Prob shape: {output['prob'].shape}")

# Test loss
loss = model.get_losses(batch, output)
print(f"Loss: {loss['overall'].item()}")
```

---

## Model Registry

### How the Registry Works

```python
from deepfakebench.metrics.registry import DETECTOR

# Register a detector
@DETECTOR.register_module(module_name='my_detector')
class MyDetector(AbstractDetector):
    pass

# Build detector from config
detector = DETECTOR.build(config)
```

### List Registered Models

```python
from deepfakebench.metrics.registry import DETECTOR

# Get all registered detectors
print(DETECTOR.module_dict.keys())
```

---

## Model Configuration

### Configuration Hierarchy

1. **Default Config**: `deepfakebench/config/train_config.yaml`
2. **Detector Config**: `deepfakebench/config/detector/<model>.yaml`
3. **Command Line**: Overrides via CLI arguments
4. **Environment Variables**: `DEEPFAKEBENCH_*`

### Key Configuration Options

```yaml
# Model identification
model_name: resnet34          # Registered model name

# Network architecture
backbone: resnet34            # Backbone network
num_classes: 2                # Output classes
pretrained: True              # Use pretrained weights

# Input configuration
resolution: 256               # Input image size
with_mask: False              # Include segmentation mask
with_landmark: False          # Include facial landmarks

# Training hyperparameters
train_batchSize: 32
test_batchSize: 64
lr: 0.0002
weight_decay: 0.0001
nEpochs: 50

# Frame sampling (for video)
frame_num:
  train: 8                    # Frames per video (training)
  test: 32                    # Frames per video (testing)
```

---

## Model Loading

### Load Pretrained Weights

```python
import torch
from deepfakebench.detectors import DETECTOR

# Build model
model = DETECTOR.build(config)

# Load checkpoint
checkpoint_path = 'deepfakebench/pretrained/resnet34_ff++.pth'
checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)

# Load state dict
model.load_state_dict(checkpoint['model_state_dict'])

# Set to evaluation mode
model.eval()
```

### Save Model Checkpoint

```python
# Save checkpoint with metadata
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'best_metric': best_auc,
    'config': config
}

torch.save(checkpoint, 'checkpoints/my_model_epoch_10.pth')
```

---

## Next Steps

- [Training Guide](TRAINING_GUIDE.md) - Train models
- [Detection Guide](DETECTION_GUIDE.md) - Run inference
- [API Reference](API_GUIDE.md) - API documentation
