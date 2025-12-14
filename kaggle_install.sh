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
echo ""
if command -v nvidia-smi &> /dev/null; then
    echo "✓ GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "  GPU Available (details unavailable)"
else
    echo "⚠ No GPU detected"
    if [ "$KAGGLE" = true ]; then
        echo "  → Make sure GPU is enabled in Notebook Settings (right panel)"
        echo "  → Go to: Settings → Accelerator → GPU T4 x2"
    fi
fi

echo ""
echo "Installing packages (using Kaggle pre-installed versions where possible)..."

# Use Kaggle's pre-installed packages and only install missing ones
echo "This may take 2-3 minutes..."
pip install -q --no-deps opencv-python 2>&1 | grep -v "dependency resolver" | grep -v "dopamine-rl" || true
pip install -q --no-deps albumentations 2>&1 | grep -v "dependency resolver" || true
pip install -q --no-deps imgaug 2>&1 | grep -v "dependency resolver" || true
pip install -q --no-deps efficientnet-pytorch 2>&1 | grep -v "dependency resolver" || true
pip install -q --no-deps timm 2>&1 | grep -v "dependency resolver" || true

# Transformers (for CLIP detectors)
echo "Installing transformers..."
pip install -q --no-deps transformers 2>&1 | grep -v "dependency resolver" || true
pip install -q --no-deps tokenizers 2>&1 | grep -v "dependency resolver" || true
pip install -q --no-deps regex 2>&1 | grep -v "dependency resolver" || true

# Additional utilities
echo "Installing additional utilities..."
pip install -q --no-deps einops loralib kornia simplejson filterpy 2>&1 | grep -v "dependency resolver" || true
pip install -q iopath 2>&1 | grep -v "dependency resolver" || true
pip install -q fvcore 2>&1 | grep -v "dependency resolver" || true
pip install -q lmdb 2>&1 | grep -v "dependency resolver" || true

# CLIP
echo "Installing CLIP..."
pip install -q --no-deps git+https://github.com/openai/CLIP.git 2>&1 | grep -v "dependency resolver" || true

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
    import os
    sys.path.insert(0, os.getcwd())
    from deepfakebench.detectors.xception_detector import XceptionDetector
    print("\n✓ DeepfakeBench modules loaded successfully!")
except Exception as e:
    print(f"\n⚠ Module import test: {e}")
    print(f"   Current directory: {os.getcwd()}")
    print(f"   Hint: Verify you're in DeepFakeBenchUpgraded folder")
EOF

if [ "$KAGGLE" = true ]; then
    echo ""
    echo "📝 Next Steps:"
    echo "  • Enable GPU: Settings → Accelerator → GPU T4 x2"
    echo "  • Datasets: Add from Kaggle Datasets or /kaggle/input/"
    echo "  • Save outputs to: /kaggle/working/"
    echo "  • GPU time limit: 30 hours/week"
    echo ""
    echo "🚀 Ready to train!"
    echo "   python deepfakebench/train.py --detector_path ./deepfakebench/config/detector/xception.yaml"
    echo ""
    echo "Note: Ignore dependency warnings (not critical for DeepfakeBench)"
fi

echo "=========================================="
