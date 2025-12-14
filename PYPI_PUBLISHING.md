# Publishing DeepfakeBench to PyPI

This guide explains how to publish the DeepfakeBench package to PyPI.

## Prerequisites

1. **PyPI Account**
   - Create account at: https://pypi.org/account/register/
   - Create account at TestPyPI: https://test.pypi.org/account/register/

2. **Install Build Tools**
   ```bash
   pip install build twine
   ```

3. **API Token**
   - Generate token at: https://pypi.org/manage/account/token/
   - Save securely for uploading

## Package Structure Preparation

### 1. Rename Directory (Important!)
```bash
# Rename 'training' to 'deepfakebench' for package name
mv training deepfakebench
```

### 2. Create __init__.py Files
```bash
# Add to deepfakebench/__init__.py
cat > deepfakebench/__init__.py << 'EOF'
"""
DeepfakeBench: Comprehensive Deepfake Detection Benchmark
"""

__version__ = "2.0.0"
__author__ = "Zhiyuan Yan, Ahmed ElBamby"

from . import detectors
from . import networks
from . import dataset

__all__ = ['detectors', 'networks', 'dataset']
EOF
```

### 3. Update Import Paths
After renaming, update all imports:
```python
# Old:
from training.detectors import XceptionDetector

# New:
from deepfakebench.detectors import XceptionDetector
```

## Building the Package

### Step 1: Clean Previous Builds
```bash
rm -rf build/ dist/ *.egg-info
```

### Step 2: Build Distribution
```bash
python -m build
```

This creates:
- `dist/deepfakebench-2.0.0-py3-none-any.whl` (wheel)
- `dist/deepfakebench-2.0.0.tar.gz` (source)

### Step 3: Test Locally
```bash
pip install dist/deepfakebench-2.0.0-py3-none-any.whl
```

## Publishing

### Test on TestPyPI First

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ deepfakebench
```

### Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Enter your PyPI username and token when prompted
```

## After Publishing

Users can install with:
```bash
# Basic installation
pip install deepfakebench

# With transformers support (CLIP detectors)
pip install deepfakebench[transformers]

# Full installation
pip install deepfakebench[all]
```

## Usage After Installation

```python
# Import the package
import deepfakebench

# Use detectors
from deepfakebench.detectors import XceptionDetector

# Command-line tools
deepfakebench-train --detector_path config/detector/xception.yaml
deepfakebench-test --detector_path config/detector/xception.yaml
```

## Version Management

Update version in both:
- `pyproject.toml`: `version = "2.0.0"`
- `setup.py`: `version='2.0.0'`
- `deepfakebench/__init__.py`: `__version__ = "2.0.0"`

## Important Notes

1. **Package Name**: Must be unique on PyPI
   - Current: `deepfakebench`
   - Alternative: `deepfakebench-upgraded`, `deepfakebench2`

2. **License**: Using CC BY-NC 4.0 (non-commercial)
   - Ensure you have rights to publish
   - Keep original authors credited

3. **Large Files**: PyPI has 100MB limit per file
   - Don't include datasets
   - Keep pretrained weights separate (download on demand)

4. **Dependencies**: All in requirements.txt
   - Keep versions flexible where possible
   - Pin critical dependencies

## Automation with GitHub Actions

Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: twine upload dist/*
```

## Testing Checklist

Before publishing:
- [ ] All imports work with new package name
- [ ] Version numbers updated everywhere
- [ ] README.md has correct installation instructions
- [ ] Tests pass: `pytest tests/`
- [ ] Built package installs: `pip install dist/*.whl`
- [ ] Command-line scripts work
- [ ] No large files (check with `du -sh dist/*`)

## Resources

- PyPI Guide: https://packaging.python.org/tutorials/packaging-projects/
- TestPyPI: https://test.pypi.org/
- PyPI: https://pypi.org/
