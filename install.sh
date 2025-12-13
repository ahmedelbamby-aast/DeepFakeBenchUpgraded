#!/bin/bash

# DeepfakeBench Installation Script
# Compatible with local environments and Kaggle notebooks
# Updated for Python 3.7-3.11 compatibility

echo "===================================="
echo "DeepfakeBench Installation"
echo "===================================="

# Core dependencies
echo "Installing core packages..."
pip install numpy==1.21.6
pip install pandas==1.3.5  # Compatible with Python 3.7
pip install Pillow==9.0.1
pip install imageio==2.9.0
pip install tqdm==4.67.1
pip install scipy==1.7.3
pip install seaborn==0.11.2
pip install pyyaml==6.0
pip install imutils==0.5.4

# Computer Vision
echo "Installing CV libraries..."
pip install opencv-python==4.6.0.66
pip install scikit-image==0.19.3
pip install scikit-learn==1.0.2
pip install albumentations==1.1.0
pip install imgaug==0.4.0

# PyTorch (adjust CUDA version as needed)
echo "Installing PyTorch..."
pip install torch==1.12.0+cu113 torchvision==0.13.0+cu113 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu113

# Deep Learning models
echo "Installing model libraries..."
pip install efficientnet-pytorch==0.7.1
pip install timm==0.6.13
pip install segmentation-models-pytorch==0.3.2
pip install torchtoolbox==0.1.8.2

# Training utilities
echo "Installing training tools..."
pip install tensorboard==2.10.1
pip install setuptools==59.5.0
pip install loralib
pip install einops
pip install filterpy
pip install simplejson
pip install kornia
pip install fvcore

# Transformers (for CLIP, X-CLIP detectors)
echo "Installing transformers..."
pip install transformers==4.30.2 --no-deps
pip install "tokenizers<0.14,>=0.11" --no-build-isolation
pip install regex

# CLIP
echo "Installing CLIP..."
pip install git+https://github.com/openai/CLIP.git

# Optional: dlib (may fail on some systems - not critical)
echo "Attempting to install dlib (optional)..."
pip install dlib==19.24.0 || echo "⚠ dlib installation failed (optional for preprocessing)"

echo ""
echo "===================================="
echo "✅ Installation Complete!"
echo "===================================="
echo ""
echo "Note: This codebase has been upgraded for:"
echo "  • PyTorch 2.x compatibility (forward-compatible)"
echo "  • Python 3.8+ support"
echo "  • Secure model loading with weights_only parameter"
echo ""
echo "Next steps:"
echo "  1. Download datasets from README links"
echo "  2. Download pretrained weights (optional)"
echo "  3. Run training or evaluation"
echo "===================================="
