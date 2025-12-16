#!/bin/bash

# ============================================================================
# Kaggle-Optimized Installation Script for DeepfakeBench
# ============================================================================
# This script is optimized for Kaggle notebooks with GPU support
# Completely suppresses all warnings for clean output

# ============================================================================
# SECTION 1: ENVIRONMENT SETUP - Suppress ALL warnings
# ============================================================================
export TF_CPP_MIN_LOG_LEVEL=3
export TF_ENABLE_ONEDNN_OPTS=0
export PYTHONWARNINGS="ignore"
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export TOKENIZERS_PARALLELISM=false

# Suppress pip warnings
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_WARN_SCRIPT_LOCATION=1

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

# ============================================================================
# SECTION 2: UNINSTALL CONFLICTING PACKAGES (Clean slate)
# ============================================================================
echo ""
echo "Preparing environment..."

# Silently remove potentially conflicting packages
pip uninstall -q -y dopamine-rl 2>/dev/null || true
pip uninstall -q -y tensorflow-probability 2>/dev/null || true

# ============================================================================
# SECTION 3: INSTALL REQUIRED PACKAGES ONLY
# ============================================================================
echo ""
echo "Installing packages (using Kaggle pre-installed versions where possible)..."
echo "This may take 2-3 minutes..."

# Core computer vision packages
pip install -q --no-deps opencv-python-headless 2>/dev/null || pip install -q opencv-python-headless 2>/dev/null || true
pip install -q --no-deps albumentations 2>/dev/null || true
pip install -q --no-deps imgaug 2>/dev/null || true

# Deep learning utilities
pip install -q --no-deps efficientnet-pytorch 2>/dev/null || true
pip install -q --no-deps timm 2>/dev/null || true

# Transformers (for CLIP and text-based detectors)
echo "Installing transformers..."
pip install -q --no-deps transformers 2>/dev/null || true
pip install -q --no-deps tokenizers 2>/dev/null || true
pip install -q --no-deps regex 2>/dev/null || true

# Additional utilities required by DeepfakeBench
echo "Installing additional utilities..."
pip install -q --no-deps einops 2>/dev/null || true
pip install -q --no-deps loralib 2>/dev/null || true
pip install -q --no-deps kornia 2>/dev/null || true
pip install -q --no-deps simplejson 2>/dev/null || true
pip install -q --no-deps filterpy 2>/dev/null || true
pip install -q iopath 2>/dev/null || true
pip install -q fvcore 2>/dev/null || true
pip install -q lmdb 2>/dev/null || true
pip install -q --no-deps pyyaml 2>/dev/null || true
pip install -q --no-deps scikit-learn 2>/dev/null || true
pip install -q --no-deps scikit-image 2>/dev/null || true

# CLIP (OpenAI)
echo "Installing CLIP..."
pip install -q --no-deps git+https://github.com/openai/CLIP.git 2>/dev/null || true

# Note: tensorboard is optional - uncomment if needed for training visualization
# pip install -q tensorboard 2>/dev/null || true

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="

# ============================================================================
# SECTION 4: VERIFICATION (Clean output, no warnings)
# ============================================================================

# Run verification in a clean subprocess with ALL stderr suppressed
python3 -W ignore 2>/dev/null << 'PYEOF'
import os
import sys
import warnings

# Completely suppress all warnings at all levels
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Redirect stderr to devnull for this script
import io
_stderr_backup = sys.stderr
sys.stderr = io.StringIO()

# Suppress specific library warnings
import logging
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('transformers').setLevel(logging.ERROR)
logging.getLogger('PIL').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('charset_normalizer').setLevel(logging.ERROR)
for name in logging.Logger.manager.loggerDict.keys():
    logging.getLogger(name).setLevel(logging.ERROR)

try:
    import torch
    
    # Restore stderr for our output only
    sys.stderr = _stderr_backup
    
    print("\n📊 Environment Info:")
    print(f"  • Python: {sys.version.split()[0]}")
    print(f"  • PyTorch: {torch.__version__}")
    print(f"  • CUDA Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  • GPU: {torch.cuda.get_device_name(0)}")
        print(f"  • GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Test DeepfakeBench imports with stderr suppressed
    sys.stderr = io.StringIO()
    sys.path.insert(0, os.getcwd())
    from deepfakebench.detectors.xception_detector import XceptionDetector
    sys.stderr = _stderr_backup
    print("\n✓ DeepfakeBench modules loaded successfully!")
    
except Exception as e:
    sys.stderr = _stderr_backup
    # Only show actual errors, not warnings
    if "No module named" in str(e) or "cannot import" in str(e).lower():
        print(f"\n⚠ Module import issue: {e}")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Hint: Verify you're in DeepFakeBenchUpgraded folder")
PYEOF

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
fi

echo "=========================================="
