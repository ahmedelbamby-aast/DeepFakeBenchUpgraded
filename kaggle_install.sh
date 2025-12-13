#!/bin/bash

# Kaggle-Optimized Installation Script for DeepfakeBench
# This script is optimized for Kaggle notebooks with GPU support

echo "=========================================="
echo "DeepfakeBench - Kaggle Quick Install"
echo "=========================================="

# Check if running on Kaggle
if [ -d "/kaggle" ]; then
    echo "✓ Detected Kaggle environment"
    KAGGLE=true
else
    echo "ℹ Running in standard environment"
    KAGGLE=false
fi

# Check GPU
if command -v nvidia-smi &> /dev/null; then
    echo "✓ GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "⚠ No GPU detected"
fi

echo ""
echo "Installing core packages..."

# Core packages (many pre-installed on Kaggle)
pip install -q opencv-python==4.6.0.66
pip install -q scikit-image==0.19.3
pip install -q scikit-learn==1.0.2
pip install -q albumentations==1.1.0
pip install -q efficientnet-pytorch==0.7.1
pip install -q timm==0.6.13
pip install -q tensorboard==2.10.1

# Transformers (for CLIP detectors)
echo "Installing transformers..."
pip install -q transformers==4.30.2 --no-deps
pip install -q "tokenizers<0.14,>=0.11" --no-build-isolation
pip install -q regex

# Additional utilities
pip install -q einops loralib kornia fvcore simplejson filterpy

# CLIP
echo "Installing CLIP..."
pip install -q git+https://github.com/openai/CLIP.git

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="

# Verification
python3 << 'EOF'
import torch
import sys

print("\n📊 Environment Info:")
print(f"  • Python: {sys.version.split()[0]}")
print(f"  • PyTorch: {torch.__version__}")
print(f"  • CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"  • GPU: {torch.cuda.get_device_name(0)}")
    print(f"  • GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Test imports
try:
    sys.path.insert(0, 'training')
    from detectors.xception_detector import XceptionDetector
    print("\n✓ DeepfakeBench modules loaded successfully!")
except Exception as e:
    print(f"\n⚠ Module import test: {e}")
EOF

if [ "$KAGGLE" = true ]; then
    echo ""
    echo "📝 Kaggle Tips:"
    echo "  • Datasets: Add from Kaggle Datasets or /kaggle/input/"
    echo "  • Save outputs to: /kaggle/working/"
    echo "  • GPU time limit: 30 hours/week"
    echo ""
    echo "🚀 Ready to train!"
    echo "   python training/train.py --detector_path ./training/config/detector/xception.yaml"
fi

echo "=========================================="
