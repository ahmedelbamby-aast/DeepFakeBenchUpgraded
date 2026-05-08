# DeepFakeBench - Quick Reference Guide

## 📚 Navigation

### 🎯 Start Here
- **New Users:** Read [README.md](README.md) → [KAGGLE_GUIDE.md](KAGGLE_GUIDE.md)
- **Developers:** Read [README.md](README.md) → [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
- **Troubleshooting:** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📖 Documentation Index

### Core Documentation
| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Main project documentation | Everyone |
| [UPDATES.md](UPDATES.md) | Version 2.0 changelog | Everyone |
| [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) | Repository organization | Everyone |

### For Users
| Document | Purpose |
|----------|---------|
| [KAGGLE_GUIDE.md](KAGGLE_GUIDE.md) | **Complete Kaggle guide** (setup, testing, troubleshooting) |
| [KAGGLE_DATASET_GUIDE.md](KAGGLE_DATASET_GUIDE.md) | Dataset structure compatibility guide |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | **Common issues and solutions** |

### For Developers
| Document | Purpose |
|----------|---------|
| [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) | **Complete development guide** (package dev, PyPI publishing, contributing) |
| [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) | Repository organization reference |

---

## 🗂️ Repository Structure at a Glance

```
DeepFakeBenchUpgraded/
│
├── deepfakebench/              📦 Main package
│   ├── detectors/              → 36+ detection models
│   ├── networks/               → Backbone architectures
│   ├── dataset/                → Data loaders (9+ datasets)
│   ├── config/                 → YAML configurations
│   ├── trainer/                → Training logic
│   ├── metrics/                → Evaluation metrics
│   ├── loss/                   → Loss functions
│   └── preprocessing/          → Data preprocessing
│
├── analysis/                   📊 Analysis scripts
├── datasets/                   💾 Dataset storage (empty)
├── figures/                    🖼️ Documentation images
│
├── *.md                        📄 Documentation files
├── requirements.txt            📋 Dependencies
├── setup.py                    ⚙️ Package configuration
└── kaggle_install.sh           🔧 Kaggle installer
```

**For detailed explanation, see [REPOSITORY_ANALYSIS.md](REPOSITORY_ANALYSIS.md)**

---

## 🚀 Common Tasks

### Install on Kaggle
```bash
!git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
%cd DeepFakeBenchUpgraded
!bash kaggle_install.sh
```
**Time:** 2-3 minutes  
**Details:** [KAGGLE_TEST.md](KAGGLE_TEST.md)

---

### Install Locally
```bash
git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
cd DeepFakeBenchUpgraded
pip install -r requirements.txt
```
**Details:** [README.md](README.md#installation)

---

### Test Installation
```python
import sys
sys.path.insert(0, '/path/to/DeepFakeBenchUpgraded')
from deepfakebench.detectors.sladd_detector import SLADDXceptionDetector
print("✓ Import successful!")
```
**Details:** [KAGGLE_TEST.md](KAGGLE_TEST.md)

---

### Use a Detector
```python
import torch
from deepfakebench.detectors.sladd_detector import SLADDXceptionDetector

config = {
    'backbone_name': 'xception_sladd',
    'backbone_config': {
        'mode': 'original',
        'num_classes': 2,
        'inc': 3,
        'dropout': False
    },
    'pretrained': 'None',
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

detector = SLADDXceptionDetector(config)
print(f"Model parameters: {sum(p.numel() for p in detector.parameters())/1e6:.2f}M")

# Forward pass
x = torch.randn(1, 3, 224, 224)
output = detector(x)
```

---

### Train a Model
```bash
python deepfakebench/train.py \
  --detector_path ./deepfakebench/config/detector/xception.yaml \
  --train_dataset "FaceForensics++" \
  --test_dataset "Celeb-DF-v1" "Celeb-DF-v2"
```
**Details:** [README.md](README.md#training)

---

### Test a Model
```bash
python deepfakebench/test.py \
  --detector_path ./deepfakebench/config/detector/xception.yaml \
  --test_dataset "Celeb-DF-v1" "Celeb-DF-v2" \
  --weights_path ./deepfakebench/weights/xception_best.pth
```
**Details:** [README.md](README.md#evaluation)

---

## 🔍 Find Information

### "How do I...?"

| Question | Answer |
|----------|--------|
| Install on Kaggle? | [KAGGLE_GUIDE.md](KAGGLE_GUIDE.md) |
| Use my own dataset? | [KAGGLE_DATASET_GUIDE.md](KAGGLE_DATASET_GUIDE.md) |
| Add a new detector? | [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md#contributing) |
| Fix import errors? | [TROUBLESHOOTING.md](TROUBLESHOOTING.md#import-errors) |
| Understand the code structure? | [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md) |
| Contribute to the project? | [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md#contributing) |
| Publish to PyPI? | [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md#publishing-to-pypi) |

---

### "What is...?"

| Term | Definition | Location |
|------|------------|----------|
| Detector | A deepfake detection model | `deepfakebench/detectors/` |
| Backbone | A neural network architecture | `deepfakebench/networks/` |
| LMDB | Fast database for image data | `deepfakebench/dataset/` |
| c23/c40 | Compression levels in FaceForensics++ | [README.md](README.md) |
| SBI | Self-Blended Images detector | `deepfakebench/detectors/sbi_detector.py` |
| SLADD | Self-supervised Learning detector | `deepfakebench/detectors/sladd_detector.py` |

---

### "Where is...?"

| Item | Location |
|------|----------|
| All detectors | `deepfakebench/detectors/*.py` |
| Configuration files | `deepfakebench/config/detector/*.yaml` |
| Dataset loaders | `deepfakebench/dataset/*.py` |
| Training script | `deepfakebench/train.py` |
| Testing script | `deepfakebench/test.py` |
| Pretrained weights | Download from [releases](https://github.com/SCLBD/DeepfakeBench/releases) |
| Analysis tools | `analysis/*.py` |
| Documentation | `*.md` files in root |

---

## ✅ What's Working

- ✅ 36+ detector models (Xception, SLADD, Effort, LSDA, etc.)
- ✅ Python 3.8-3.12 support
- ✅ PyTorch 2.x compatible
- ✅ Kaggle optimized (2-3 min install)
- ✅ 9+ supported datasets
- ✅ Comprehensive documentation
- ✅ Clean package structure
- ✅ LMDB fast loading
- ✅ Multi-GPU training (DDP)
- ✅ Optional TensorBoard support

**Details:** [REPOSITORY_ANALYSIS.md](REPOSITORY_ANALYSIS.md#-whats-working-well)

---

## ⚠️ Known Issues

### Minor Issues
1. **SlowFast warning on import** - Non-critical, only affects SlowFast detector
   - **Fix:** Install `simplejson` (already in requirements.txt)

2. **Pretrained weights not included** - Must download separately
   - **Workaround:** Download from [releases](https://github.com/SCLBD/DeepfakeBench/releases)

3. **dlib model file missing** - Only needed for preprocessing
   - **Workaround:** Download from link in README

**Full List:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 💡 Recommended Improvements

### High Priority
1. **Create API Documentation** - Use Sphinx (4-6 hours)
2. **Add Tutorial Notebooks** - 3-4 examples (8-12 hours)
3. **Update Installation Script** - Ensure all deps installed (30 min)

### Medium Priority
4. **Add CONTRIBUTING.md** - Contribution guide (2-3 hours)
5. **Document Analysis Scripts** - Add README in analysis/ (2-3 hours)
6. **Dataset Download Helper** - Auto-download script (6-8 hours)

**See Development Guide:** [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)

---

## 📊 Repository Stats

- **Version:** 2.0.0
- **License:** CC BY-NC 4.0
- **Python Support:** 3.8-3.12
- **PyTorch Support:** 2.x
- **Detectors:** 36+
- **Datasets:** 9+
- **Python Files:** 150+
- **Documentation Files:** 13+

---

## 🔗 Important Links

- **This Repository:** https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded
- **Original Repository:** https://github.com/SCLBD/DeepfakeBench
- **Research Paper:** https://arxiv.org/abs/2307.01426
- **Pretrained Weights:** https://github.com/SCLBD/DeepfakeBench/releases
- **Issues:** https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues

---

## 🆘 Getting Help

1. **Read the docs:** Start with [REPOSITORY_ANALYSIS.md](REPOSITORY_ANALYSIS.md)
2. **Check existing issues:** Look for similar problems
3. **Try troubleshooting:** See [KAGGLE_FIXES.md](KAGGLE_FIXES.md)
4. **Ask for help:** Open an issue on GitHub

---

## 📝 Key Takeaways

### For Users
- ✅ **Production ready** - Works on Kaggle, Colab, and local
- ✅ **Easy to install** - 2-3 minutes on Kaggle
- ✅ **Well documented** - Comprehensive guides available
- ⚠️ **Download weights separately** - Not included in repo

### For Developers
- ✅ **Clean codebase** - Well-organized and consistent
- ✅ **Modern Python** - Compatible with latest versions
- ✅ **Extensible** - Easy to add new detectors
- ⚠️ **Limited API docs** - Need to read source code

### For Researchers
- ✅ **36+ models** - Comprehensive detector collection
- ✅ **9+ datasets** - Extensive evaluation support
- ✅ **Unified framework** - Consistent training/testing
- ⚠️ **Manual preprocessing** - Dataset setup required

---

## 🎯 Next Steps

### If You're New
1. Read [README.md](README.md)
2. Try [KAGGLE_GUIDE.md](KAGGLE_GUIDE.md) quick start
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if needed

### If You Want to Train
1. Download datasets (see [README.md](README.md))
2. Generate JSON mappings (see [KAGGLE_DATASET_GUIDE.md](KAGGLE_DATASET_GUIDE.md))
3. Configure training (see [README.md](README.md#training))
4. Start training!

### If You Want to Contribute
1. Read [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
2. Review contributing guidelines
3. Pick an improvement to work on
4. Open a pull request

---

## 📌 Version Information

- **Document Version:** 1.0
- **Repository Version:** 2.0.0
- **Last Updated:** December 16, 2025
- **Status:** Complete and Current

---

**Need more details?** See the comprehensive guides in the documentation files above 📖
