# Quick Model Integration Reference

## TL;DR - Add Your Model in 3 Steps

### Step 1️⃣: Place Your Model Weights
```bash
cp your_model.pth deepfakebench/pretrained/my_model.pth
```

### Step 2️⃣: Create Configuration (YAML)
**File:** `deepfakebench/config/detector/my_model.yaml`
```yaml
model_name: my_model
backbone: resnet34
num_classes: 2
pretrained: True
resolution: 256
train_batchSize: 32
test_batchSize: 64
lr: 0.0002
nEpochs: 50
```

### Step 3️⃣: Use Your Model
```python
from deepfakebench.api import Detector
detector = Detector(model='my_model')
result = detector(image)
```

---

## Directory Structure Reference

```
deepfakebench/
├── pretrained/                          # 📁 Model weights location
│   ├── xception-b5690688.pth           # (existing)
│   ├── resnet34-b627a593.pth           # (existing)
│   └── my_model.pth                    # ➕ YOUR WEIGHTS HERE
│
├── config/
│   └── detector/                        # 📁 Model configs
│       ├── xception.yaml               # (existing)
│       ├── resnet34.yaml               # (existing)
│       └── my_model.yaml               # ➕ YOUR CONFIG HERE
│
└── detectors/                           # 📁 Model implementations (optional)
    ├── base_detector.py                # (don't modify)
    ├── xception_detector.py            # (existing)
    └── my_custom_detector.py           # ➕ OPTIONAL: Your code here
```

---

## Checklist

- [ ] Model weights file (`.pth`) placed in `deepfakebench/pretrained/`
- [ ] Configuration file (`.yaml`) created in `deepfakebench/config/detector/`
- [ ] Config has `model_name`, `backbone`, `num_classes`, `pretrained` fields
- [ ] Tested with: `Detector(model='my_model')`
- [ ] (Optional) Custom model code in `deepfakebench/detectors/`

---

## Full Guide

📖 **Read the complete guide:** [docs/CUSTOM_MODELS_GUIDE.md](CUSTOM_MODELS_GUIDE.md)

### Includes:
- ✅ Two scenarios (weights-only vs. custom code)
- ✅ Complete working examples with explanations
- ✅ All required vs. optional files
- ✅ Common issues & troubleshooting
- ✅ FAQ section
- ✅ Model file format specifications

---

## Model File Format

| Filename | Location | Required | Format |
|----------|----------|----------|--------|
| `my_model.pth` | `deepfakebench/pretrained/` | ✅ | PyTorch state dict or checkpoint |
| `my_model.yaml` | `deepfakebench/config/detector/` | ✅ | YAML configuration |
| `my_custom_detector.py` | `deepfakebench/detectors/` | ❌ | Python class (if custom) |

---

## Example Configurations

### Minimal Configuration
```yaml
model_name: my_model
backbone: resnet34
num_classes: 2
resolution: 256
```

### Complete Configuration
```yaml
model_name: my_detector
backbone: resnet34
num_classes: 2
pretrained: True
resolution: 256

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

# Augmentation
augment:
  flip_prob: 0.5
  brightness: 0.2
  contrast: 0.2

# Frames (for video)
frame_num:
  train: 8
  test: 32

# Loss
loss_weights:
  cls: 1.0

# Metrics
metric_scoring: auc
```

---

## Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| Config not found | ✅ File must be in `deepfakebench/config/detector/` |
| Model not loading | ✅ Check weights format: `.pth` file with `state_dict` |
| Wrong predictions | ✅ Verify input preprocessing matches training |
| Out of memory | ✅ Reduce `train_batchSize` and `resolution` in YAML |
| Module not found | ✅ Ensure import in `deepfakebench/detectors/__init__.py` |

**For detailed help:** See [CUSTOM_MODELS_GUIDE.md#troubleshooting](CUSTOM_MODELS_GUIDE.md#troubleshooting)

---

**Last Updated:** December 2025
