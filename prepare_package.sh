#!/bin/bash

# DeepfakeBench Package Preparation Script
# Prepares the codebase for PyPI publication

set -e  # Exit on error

echo "=========================================="
echo "DeepfakeBench - PyPI Package Preparation"
echo "=========================================="

# Step 1: Check prerequisites
echo ""
echo "Step 1: Checking prerequisites..."
command -v python >/dev/null 2>&1 || { echo "Python not found!"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "Git not found!"; exit 1; }

echo "✓ Python found: $(python --version)"
echo "✓ Git found"

# Step 2: Install build tools
echo ""
echo "Step 2: Installing build tools..."
pip install -q --upgrade pip build twine

echo "✓ Build tools installed"

# Step 3: Clean previous builds
echo ""
echo "Step 3: Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info deepfakebench.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

echo "✓ Cleaned"

# Step 4: Check if training directory exists
if [ -d "training" ] && [ ! -d "deepfakebench" ]; then
    echo ""
    echo "Step 4: Renaming 'training' to 'deepfakebench'..."
    echo "⚠ This will modify your directory structure!"
    echo "Press Ctrl+C to cancel, or Enter to continue..."
    read
    
    cp -r training deepfakebench
    echo "✓ Created deepfakebench/ (kept deepfakebench/ as backup)"
    echo "  You can remove deepfakebench/ after verifying"
elif [ -d "deepfakebench" ]; then
    echo ""
    echo "Step 4: Package directory exists ✓"
else
    echo ""
    echo "❌ Error: Neither 'training' nor 'deepfakebench' directory found!"
    exit 1
fi

# Step 5: Create __init__.py
echo ""
echo "Step 5: Creating package __init__.py..."
cat > deepfakebench/__init__.py << 'EOF'
"""
DeepfakeBench: A Comprehensive Benchmark of Deepfake Detection
Upgraded for PyTorch 2.x and Python 3.8+ compatibility

Original authors: Zhiyuan Yan, Yong Zhang, Xinhang Yuan, Siwei Lyu, Baoyuan Wu
Upgraded by: Ahmed ElBamby
"""

__version__ = "2.0.0"
__author__ = "Zhiyuan Yan, Ahmed ElBamby"
__description__ = "Comprehensive Deepfake Detection Benchmark"

# Import main modules
from . import detectors
from . import networks
from . import dataset
from . import trainer

__all__ = ['detectors', 'networks', 'dataset', 'trainer']
EOF

echo "✓ Created __init__.py"

# Step 6: Validate setup.py
echo ""
echo "Step 6: Validating setup files..."
python setup.py check

echo "✓ Setup validated"

# Step 7: Build package
echo ""
echo "Step 7: Building package..."
python -m build

echo "✓ Package built successfully!"
echo ""
echo "Created files:"
ls -lh dist/

# Step 8: Test installation
echo ""
echo "Step 8: Testing local installation..."
pip install --force-reinstall dist/*.whl

echo "✓ Test installation successful!"

# Step 9: Test import
echo ""
echo "Step 9: Testing package import..."
python -c "import deepfakebench; print(f'✓ DeepfakeBench v{deepfakebench.__version__} imported successfully!')"

echo ""
echo "=========================================="
echo "✅ Package Preparation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Test thoroughly: python -c 'from deepfakebench.detectors import XceptionDetector'"
echo "  2. Upload to TestPyPI: twine upload --repository testpypi dist/*"
echo "  3. Test from TestPyPI: pip install --index-url https://test.pypi.org/simple/ deepfakebench"
echo "  4. Upload to PyPI: twine upload dist/*"
echo ""
echo "See PYPI_PUBLISHING.md for detailed instructions"
echo "=========================================="
