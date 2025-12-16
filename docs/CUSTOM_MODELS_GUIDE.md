# Custom Models Integration Guide

Complete guide for users who want to add their own deepfake detection models to the DeepFakeBench system.

## Table of Contents

1. [Quick Overview](#quick-overview)
2. [Directory Structure](#directory-structure)
3. [Step-by-Step Integration](#step-by-step-integration)
4. [Using Your Custom Model](#using-your-custom-model)
5. [Model File Requirements](#model-file-requirements)
6. [Frequently Asked Questions](#frequently-asked-questions)
7. [Troubleshooting](#troubleshooting)

---

## Quick Overview

To add a custom model to DeepFakeBench, you need to:

1. **Place model weights** → `deepfakebench/pretrained/` or `checkpoints/`
2. **Create model code** → `deepfakebench/detectors/` (if building from scratch)
3. **Create configuration file** → `deepfakebench/config/detector/`
4. **Register the model** → Import in `deepfakebench/detectors/__init__.py`
5. **Test it** → Use the Detector API

If you only have **pretrained weights** (no need to implement), skip steps 2 and 4.

---

## Directory Structure

### Where to Put Your Model Files

```
DeepFakeBenchUpgraded/
├── deepfakebench/
│   ├── detectors/                    # ← Model implementations
│   │   ├── __init__.py
│   │   ├── base_detector.py          # Base class (don't modify)
│   │   ├── xception_detector.py      # Example
│   │   └── my_custom_detector.py     # ← YOUR NEW MODEL CODE
│   │
│   ├── config/
│   │   └── detector/
│   │       ├── xception.yaml         # Example
│   │       └── my_custom_model.yaml  # ← YOUR CONFIG FILE
│   │
│   └── pretrained/                   # ← Model Weights Storage
│       ├── xception-b5690688.pth
│       ├── resnet34-b627a593.pth
│       └── my_custom_model.pth       # ← YOUR WEIGHTS
│
├── checkpoints/                       # ← Alternative location
│   └── my_model_checkpoint.pth
│
└── logs/                             # ← Training outputs
```

### Important Paths

| Location | Purpose | When to Use |
|----------|---------|------------|
| `deepfakebench/pretrained/` | Pretrained/pre-downloaded weights | For models you train or download |
| `checkpoints/` | Training checkpoints | For models in active development |
| `deepfakebench/detectors/` | Model implementation code | Only if implementing new model |
| `deepfakebench/config/detector/` | Configuration files | **Always needed** |

---

## Step-by-Step Integration

### Scenario 1: Using Pretrained Weights Only (No Code Implementation)

If you have a PyTorch model checkpoint (`.pth` file) that you want to use without implementing the model class:

#### Step 1: Prepare Your Weights

```bash
# Copy your model weights to the pretrained directory
cp /path/to/your/model.pth deepfakebench/pretrained/my_model.pth

# Or download and place it there manually
# File size: Any size (Recommended: < 500MB for fast loading)
```

**Expected format:**
- `.pth` file (PyTorch format)
- Contains `state_dict` or can be loaded directly

#### Step 2: Create Configuration File

Create `deepfakebench/config/detector/my_model.yaml`:

```yaml
# My Custom Model Configuration
# ===============================
# This configuration file tells DeepFakeBench how to use your model

# Basic model information
model_name: my_model                      # Unique identifier for your model
backbone: resnet34                        # Base architecture (if applicable)
num_classes: 2                            # Output classes (fake/real = 2)
pretrained: True                          # Use pretrained weights

# File paths
pretrained_weights: deepfakebench/pretrained/my_model.pth  # ← YOUR WEIGHTS PATH

# Input settings
resolution: 256                           # Input image size (pixels)
with_mask: False                          # Does your model use face masks?
with_landmark: False                      # Does your model use facial landmarks?

# Inference settings
inference_batchSize: 32                   # How many images to process at once
test_batchSize: 64                        # Test batch size
device: cuda                              # cuda, cpu, or auto

# Training settings (if you want to fine-tune)
train_batchSize: 32                       # Training batch size
lr: 0.0002                                # Learning rate
weight_decay: 0.0001                      # L2 regularization
nEpochs: 50                               # Number of training epochs

# Optimizer
optimizer:
  type: Adam                              # Adam optimizer
  betas: [0.9, 0.999]                    # Adam momentum parameters

# Learning rate scheduler
scheduler:
  type: CosineAnnealingLR                # Learning rate decay strategy
  T_max: 50                              # Maximum iterations
  eta_min: 0.00001                       # Minimum learning rate

# Data augmentation
augment:
  flip_prob: 0.5                         # Probability of horizontal flip
  brightness: 0.2                        # Brightness adjustment range
  contrast: 0.2                          # Contrast adjustment range

# Video frame settings
frame_num:
  train: 8                               # Frames per video during training
  test: 32                               # Frames per video during testing

# Loss configuration
loss_weights:
  cls: 1.0                               # Classification loss weight

# Metrics
metric_scoring: auc                      # Primary metric (auc, accuracy, f1)
```

#### Step 3: Test Your Model (Pretrained Weights Only)

```python
from deepfakebench.api import Detector
import torch

# Load your model
detector = Detector(model='my_model')

# Test on an image
import cv2
image = cv2.imread('test_image.jpg')

# Run inference
result = detector(image)
print(f"Prediction: {result}")
print(f"Confidence: {result['confidence']}")
```

---

### Scenario 2: Implementing a Custom Model Class

If you want to implement a custom model architecture with your own code:

#### Step 1: Implement the Model Class

Create `deepfakebench/detectors/my_custom_detector.py`:

```python
"""
My Custom Deepfake Detector
===========================

Author: Your Name
Date: YYYY-MM-DD
Description: Brief description of what makes your detector special

Features:
- Custom architecture
- Novel loss function
- Specific preprocessing
"""

import torch
import torch.nn as nn
from .base_detector import AbstractDetector
from deepfakebench.metrics.registry import DETECTOR


@DETECTOR.register_module(module_name='my_custom_detector')
class MyCustomDetector(AbstractDetector):
    """
    My Custom Deepfake Detector Implementation.
    
    This detector combines [describe your approach].
    
    Args:
        config (dict): Configuration dictionary containing:
            - backbone: Name of backbone network
            - num_classes: Number of output classes (default: 2)
            - pretrained: Whether to use pretrained weights
            - resolution: Input image resolution
    
    Example:
        >>> config = {'backbone': 'resnet34', 'num_classes': 2}
        >>> detector = MyCustomDetector(config)
        >>> image = torch.randn(1, 3, 256, 256)
        >>> output = detector({'image': image})
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Extract configuration parameters
        self.num_classes = config.get('num_classes', 2)
        self.backbone_name = config.get('backbone', 'resnet34')
        self.resolution = config.get('resolution', 256)
        
        # Build network components
        self.backbone = self._build_backbone()
        self.classifier = self._build_classifier()
        self.loss_fn = nn.CrossEntropyLoss()
    
    def _build_backbone(self):
        """
        Build feature extraction backbone.
        
        Returns:
            nn.Module: Backbone network
        """
        if self.backbone_name == 'resnet34':
            from torchvision.models import resnet34, ResNet34_Weights
            backbone = resnet34(weights=ResNet34_Weights.DEFAULT)
            # Remove the final fully connected layer
            backbone.fc = nn.Identity()
            return backbone
        
        elif self.backbone_name == 'xception':
            from torchvision.models import densenet121, DenseNet121_Weights
            backbone = densenet121(weights=DenseNet121_Weights.DEFAULT)
            backbone.classifier = nn.Identity()
            return backbone
        
        else:
            raise ValueError(f"Unknown backbone: {self.backbone_name}")
    
    def _build_classifier(self):
        """
        Build classification head.
        
        Returns:
            nn.Sequential: Classification head
        """
        return nn.Sequential(
            nn.Linear(512, 256),           # Reduce dimensions
            nn.BatchNorm1d(256),           # Normalize
            nn.ReLU(inplace=True),         # Activation
            nn.Dropout(0.5),               # Regularization
            nn.Linear(256, 128),           # Further reduction
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(128, self.num_classes)  # Final output
        )
    
    def forward(self, data_dict: dict, inference: bool = False) -> dict:
        """
        Forward pass of the model.
        
        Args:
            data_dict (dict): Dictionary containing:
                - 'image': Input tensor of shape (B, C, H, W)
                - 'label': (optional) Ground truth labels
            inference (bool): Whether in inference mode
        
        Returns:
            dict: Dictionary containing:
                - 'cls': Raw logits (B, num_classes)
                - 'prob': Probability of fake class (B,)
                - 'feat': Features from backbone (B, 512)
        
        Example:
            >>> data = {'image': torch.randn(4, 3, 256, 256)}
            >>> output = model(data)
            >>> print(output['prob'].shape)  # torch.Size([4])
        """
        # Extract input image
        x = data_dict['image']  # Shape: (B, 3, H, W)
        
        # Forward through backbone
        features = self.backbone(x)  # Shape: (B, 512)
        
        # Forward through classifier
        logits = self.classifier(features)  # Shape: (B, num_classes)
        
        # Calculate softmax probabilities
        probs = torch.softmax(logits, dim=1)
        
        # Extract probability of fake class (index 1)
        fake_prob = probs[:, 1]  # Shape: (B,)
        
        return {
            'cls': logits,           # For cross-entropy loss
            'prob': fake_prob,       # For metrics (0.0 = real, 1.0 = fake)
            'feat': features         # For feature analysis
        }
    
    def get_losses(self, data_dict: dict, pred_dict: dict) -> dict:
        """
        Calculate training losses.
        
        Args:
            data_dict (dict): Contains 'label' tensor
            pred_dict (dict): Contains 'cls' from forward pass
        
        Returns:
            dict: Dictionary of losses (must have 'overall' key)
        
        Example:
            >>> losses = model.get_losses(data, predictions)
            >>> print(losses['overall'].item())
        """
        # Get ground truth labels
        label = data_dict['label']
        
        # Calculate classification loss
        cls_loss = self.loss_fn(pred_dict['cls'], label)
        
        return {
            'overall': cls_loss,  # Main loss for backprop
            'cls': cls_loss       # Specific loss component
        }
    
    def get_train_metrics(self, data_dict: dict, pred_dict: dict) -> dict:
        """
        Calculate metrics during training.
        
        Args:
            data_dict (dict): Contains ground truth 'label'
            pred_dict (dict): Contains predictions 'prob'
        
        Returns:
            dict: Dictionary of metrics
        
        Example:
            >>> metrics = model.get_train_metrics(data, predictions)
            >>> print(metrics['acc'])
        """
        # Get labels
        label = data_dict['label']
        
        # Make binary predictions (threshold at 0.5)
        predictions = (pred_dict['prob'] > 0.5).long()
        
        # Calculate accuracy
        accuracy = (predictions == label).float().mean()
        
        return {'acc': accuracy.item()}


# Optional: Add custom data preprocessing
def preprocess_image(image_array):
    """
    Preprocess image for your model.
    
    Args:
        image_array: Input image (numpy array or PIL Image)
    
    Returns:
        torch.Tensor: Preprocessed image ready for model
    """
    import torch
    from torchvision import transforms
    
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
        transforms.Resize((256, 256))
    ])
    
    if isinstance(image_array, np.ndarray):
        image_array = Image.fromarray(image_array)
    
    return preprocess(image_array)
```

#### Step 2: Register Your Model

Edit `deepfakebench/detectors/__init__.py` and add:

```python
# Add this line with other imports
from .my_custom_detector import MyCustomDetector

# The @DETECTOR.register_module decorator in your code
# already registers it, but you can verify with:
# python -c "from deepfakebench.detectors import DETECTOR; print(DETECTOR.module_dict.keys())"
```

#### Step 3: Create Configuration File

Create `deepfakebench/config/detector/my_custom_detector.yaml`:

```yaml
# My Custom Detector Configuration
# ===================================

model_name: my_custom_detector
backbone: resnet34
num_classes: 2
pretrained: True

# Input
resolution: 256
with_mask: False
with_landmark: False

# Training
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

# Augmentation
augment:
  flip_prob: 0.5
  brightness: 0.2
  contrast: 0.2

# Video frames
frame_num:
  train: 8
  test: 32

# Loss
loss_weights:
  cls: 1.0

# Metrics
metric_scoring: auc
```

#### Step 4: Test Your Custom Model

```python
# Test that your model loads and works
from deepfakebench.detectors import DETECTOR
import torch

# Build model from config
config = {
    'model_name': 'my_custom_detector',
    'backbone': 'resnet34',
    'num_classes': 2,
    'resolution': 256
}

model = DETECTOR.build(config)

# Test forward pass
test_data = {
    'image': torch.randn(4, 3, 256, 256),
    'label': torch.tensor([0, 1, 0, 1])
}

output = model(test_data)
print(f"✓ Model forward pass successful!")
print(f"  - Logits shape: {output['cls'].shape}")
print(f"  - Probabilities shape: {output['prob'].shape}")
print(f"  - Features shape: {output['feat'].shape}")

# Test loss calculation
loss = model.get_losses(test_data, output)
print(f"✓ Loss calculation successful!")
print(f"  - Overall loss: {loss['overall'].item():.4f}")

# Test metrics
metrics = model.get_train_metrics(test_data, output)
print(f"✓ Metrics calculation successful!")
print(f"  - Accuracy: {metrics['acc']:.4f}")
```

---

## Using Your Custom Model

### Quick Start

```python
from deepfakebench.api import Detector
import cv2

# Initialize detector
detector = Detector(model='my_model')

# Load image
image = cv2.imread('test.jpg')

# Get prediction
result = detector(image)

print(f"Is Fake: {result['label']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Probabilities: {result['prob_dict']}")
```

### Training Your Model

```bash
python deepfakebench/train.py \
    --detector_path deepfakebench/config/detector/my_custom_detector.yaml \
    --data_path datasets/ \
    --save_dir checkpoints/
```

### Testing/Inference

```bash
python deepfakebench/test.py \
    --detector_path deepfakebench/config/detector/my_custom_detector.yaml \
    --weights_path checkpoints/my_custom_detector_best.pth \
    --data_path datasets/test/
```

---

## Model File Requirements

### Minimum Files Needed

| File | Required | Location | Description |
|------|----------|----------|-------------|
| YAML Config | ✅ Always | `deepfakebench/config/detector/` | Configuration file |
| `.pth` Weights | ⚠️ For inference | `deepfakebench/pretrained/` | Pretrained weights |
| Model Code | ⚠️ If custom | `deepfakebench/detectors/` | Implementation file |

### Configuration File Structure

Every model **must** have a corresponding YAML configuration:

```yaml
# Required fields
model_name: unique_name                   # ✅ REQUIRED
backbone: architecture_name               # ✅ REQUIRED
num_classes: 2                            # ✅ REQUIRED
pretrained: true                          # ✅ REQUIRED

# Recommended fields
resolution: 256
train_batchSize: 32
test_batchSize: 64
lr: 0.0002
nEpochs: 50

# Optional fields
with_mask: false
with_landmark: false
augment: {...}
```

### Weight File Format

- **Format**: PyTorch `.pth` or `.pt` file
- **Size**: Recommended < 500MB (faster loading)
- **Content**: Either:
  - Direct model state dict (keys like `module.1.weight`)
  - Checkpoint dictionary with `'model_state_dict'` key
- **Example**:

```python
# Save your model weights
torch.save(model.state_dict(), 'my_model.pth')

# Or save as checkpoint
checkpoint = {
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': 50,
    'best_auc': 0.97
}
torch.save(checkpoint, 'my_model_checkpoint.pth')
```

---

## Frequently Asked Questions

### Q1: Can I use models from other frameworks (TensorFlow, ONNX)?

**A:** Currently, DeepFakeBench requires PyTorch models. Options:

1. **Convert to PyTorch** using libraries like:
   - `onnx2pytorch` for ONNX models
   - `tensorflow2pytorch` for TensorFlow models

2. **Implement wrapper** in `my_detector.py`:
   ```python
   import torch
   import onnx
   import onnxruntime
   
   class WrappedDetector(AbstractDetector):
       def __init__(self, config):
           super().__init__(config)
           self.session = onnxruntime.InferenceSession('model.onnx')
       
       def forward(self, data_dict):
           # Run ONNX inference
           output = self.session.run(None, {'input': data_dict['image'].numpy()})
           return {'prob': torch.tensor(output[0])}
   ```

### Q2: Where do I put my training data?

**A:** See [DATASET_GUIDE.md](DATASET_GUIDE.md). Default locations:

```
datasets/
├── train/
│   ├── fake/
│   └── real/
├── val/
│   ├── fake/
│   └── real/
└── test/
    ├── fake/
    └── real/
```

### Q3: What if my model takes different input (e.g., video sequences)?

**A:** Modify the `forward` method to handle your input format:

```python
def forward(self, data_dict, inference=False):
    # Handle video input (B, T, C, H, W)
    if 'video' in data_dict:
        x = data_dict['video']  # Shape: (B, T, 3, H, W)
        # Process frames...
    else:
        x = data_dict['image']  # Shape: (B, C, H, W)
    
    # Rest of your implementation
```

### Q4: How do I add multiple models at once?

**A:** Repeat the process for each model. Example with 3 models:

```
deepfakebench/config/detector/
├── model_a.yaml
├── model_b.yaml
└── model_c.yaml

deepfakebench/detectors/
├── model_a_detector.py      (if custom)
├── model_b_detector.py      (if custom)
└── model_c_detector.py      (if custom)

deepfakebench/pretrained/
├── model_a.pth
├── model_b.pth
└── model_c.pth
```

### Q5: Can I use GPU acceleration?

**A:** Yes! Set in configuration:

```yaml
device: cuda  # or auto (auto-detects)
mixed_precision: true  # Optional: faster training
```

Or programmatically:

```python
detector = Detector(model='my_model', device='cuda')
```

### Q6: How do I compare my model with existing ones?

**A:** Use the benchmark script:

```python
from deepfakebench.api import Detector
import time

models = ['xception', 'my_custom_detector', 'efficientnetb4']

for model_name in models:
    detector = Detector(model=model_name)
    
    # Benchmark
    start = time.time()
    result = detector(image)
    elapsed = time.time() - start
    
    print(f"{model_name}: {elapsed:.3f}s, Confidence: {result['confidence']:.2%}")
```

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'my_detector'"

**Solution:**
1. Ensure file is in `deepfakebench/detectors/`
2. Add import to `deepfakebench/detectors/__init__.py`
3. Verify class decorator: `@DETECTOR.register_module(module_name='my_detector')`

```python
# Check registration
from deepfakebench.metrics.registry import DETECTOR
print(DETECTOR.module_dict.keys())  # Should include 'my_detector'
```

### Issue 2: "Config file not found" error

**Solution:** Ensure YAML file is in correct location:

```bash
# Correct location
deepfakebench/config/detector/my_model.yaml

# NOT in these locations:
deepfakebench/config/my_model.yaml          ✗
deepfakebench/my_model.yaml                 ✗
```

### Issue 3: Model weights fail to load

**Check weight file format:**

```python
import torch

# Check if weights load
try:
    weights = torch.load('my_model.pth', map_location='cpu')
    print("✓ Weights loaded successfully")
    print(f"  Keys: {weights.keys()}")
except Exception as e:
    print(f"✗ Failed to load: {e}")

# If checkpoint format:
if isinstance(weights, dict) and 'model_state_dict' in weights:
    model.load_state_dict(weights['model_state_dict'])
else:
    model.load_state_dict(weights)
```

### Issue 4: Out of memory (OOM) errors

**Solutions:**
1. Reduce batch size in config:
   ```yaml
   train_batchSize: 8    # Reduced from 32
   test_batchSize: 16
   ```

2. Reduce input resolution:
   ```yaml
   resolution: 128       # Reduced from 256
   ```

3. Use gradient accumulation:
   ```yaml
   gradient_accumulation_steps: 4
   ```

### Issue 5: Accuracy too low or predictions all zeros

**Check:**
1. Verify input preprocessing matches training:
   ```python
   # Ensure normalization values match
   transforms.Normalize(
       mean=[0.485, 0.456, 0.406],
       std=[0.229, 0.224, 0.225]
   )
   ```

2. Verify output format in `forward()`:
   ```python
   return {
       'cls': logits,                    # Shape: (B, 2)
       'prob': fake_prob,                # Shape: (B,) with values 0-1
       'feat': features
   }
   ```

3. Check if model is in eval mode:
   ```python
   model.eval()  # Disable dropout, batch norm
   with torch.no_grad():
       output = model(test_data)
   ```

### Issue 6: "Key mismatch" when loading weights

**Solution:** Ensure architecture matches weights:

```python
# Diagnose mismatch
model = MyDetector(config)
checkpoint = torch.load('weights.pth')

model_keys = set(model.state_dict().keys())
checkpoint_keys = set(checkpoint.keys())

print("Missing from checkpoint:", model_keys - checkpoint_keys)
print("Extra in checkpoint:", checkpoint_keys - model_keys)

# Load with partial match if needed
model.load_state_dict(checkpoint, strict=False)
```

---

## Next Steps

After adding your model:

1. **Test** it with sample images
2. **Train** on benchmark datasets (FF++, CelebDF)
3. **Compare** performance with existing models
4. **Share** your model configuration in community discussions
5. **Contribute** back if you've achieved great results!

For more information:
- [API Guide](API_GUIDE.md) - Using the Detector API
- [Dataset Guide](DATASET_GUIDE.md) - Working with datasets
- [MODEL_GUIDE.md](MODEL_GUIDE.md) - Technical model details
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Environment setup

---

**Last Updated:** December 2025
**Version:** 1.0
