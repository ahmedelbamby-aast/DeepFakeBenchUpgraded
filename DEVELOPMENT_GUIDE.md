# 🛠️ Development Guide for DeepFakeBench

> Complete guide for developers, contributors, and maintainers

---

## 📋 Table of Contents

- [Package Development](#-package-development)
- [Converting to Pip Package](#-converting-to-pip-package)
- [Publishing to PyPI](#-publishing-to-pypi)
- [Contributing](#-contributing)
- [Development Setup](#-development-setup)
- [Testing](#-testing)

---

## 📦 Package Development

### Current Package Structure

```
deepfakebench/
├── __init__.py                 # Package initialization (v2.0.0)
├── train.py                    # Training entry point
├── test.py                     # Testing entry point
├── config/                     # Configuration files (YAML)
├── dataset/                    # Dataset loaders and utilities
├── detectors/                  # 36+ detector implementations
├── networks/                   # Backbone networks
├── loss/                       # Loss functions
├── metrics/                    # Evaluation metrics
├── trainer/                    # Training logic
└── preprocessing/              # Data preprocessing scripts
```

### Package Features

✅ **Modern Python Packaging** - Uses `pyproject.toml` and `setup.py`  
✅ **Pip Installable** - `pip install -e .` for development  
✅ **Entry Points** - CLI commands: `deepfakebench-train`, `deepfakebench-test`  
✅ **Version Management** - Centralized in `__init__.py`  
✅ **Dependencies** - Flexible version requirements  

### Package Installation Modes

#### Development Mode (Editable)
```bash
# Clone repository
git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
cd DeepFakeBenchUpgraded

# Install in editable mode
pip install -e .

# Changes to code are immediately available
```

#### User Mode (Standard)
```bash
# Install from source
pip install .

# Or from GitHub
pip install git+https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
```

#### With Optional Dependencies
```bash
# Install with transformers support (CLIP detectors)
pip install -e ".[transformers]"

# Install development tools
pip install -e ".[dev]"

# Install everything
pip install -e ".[all]"
```

---

## 🚀 Converting to Pip Package

### Quick Steps Summary

1. **Prepare Files** (✅ Already done)
2. **Build Package** (2 min)
3. **Test Locally** (5 min)
4. **Publish** (5 min)

### Step 1: Package Files (Already Prepared)

These files are already configured:

- ✅ `setup.py` - Package configuration
- ✅ `pyproject.toml` - Modern Python packaging
- ✅ `MANIFEST.in` - File inclusion rules
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Package documentation

### Step 2: Build Package

```bash
# Install build tools
pip install build twine

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build distribution
python -m build
```

This creates:
- `dist/deepfakebench-2.0.0-py3-none-any.whl` (wheel)
- `dist/deepfakebench-2.0.0.tar.gz` (source)

### Step 3: Test Locally

```bash
# Install from wheel
pip install dist/deepfakebench-2.0.0-py3-none-any.whl

# Test import
python -c "from deepfakebench.detectors import XceptionDetector; print('✓ Works!')"

# Test CLI
deepfakebench-train --help
```

### Step 4: Verify Package Contents

```bash
# List files in wheel
unzip -l dist/deepfakebench-2.0.0-py3-none-any.whl

# Check package metadata
pip show deepfakebench
```

---

## 📤 Publishing to PyPI

### Prerequisites

1. **PyPI Account**
   - Create account at: https://pypi.org/account/register/
   - Create account at TestPyPI: https://test.pypi.org/account/register/

2. **API Token**
   - Generate token at: https://pypi.org/manage/account/token/
   - Save securely (you'll need it for uploading)

3. **Build Tools**
   ```bash
   pip install build twine
   ```

### Publishing Process

#### Step 1: Test on TestPyPI First

```bash
# Build package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
# Enter username: __token__
# Enter password: <your-testpypi-token>

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ deepfakebench
```

#### Step 2: Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
# Enter username: __token__
# Enter password: <your-pypi-token>
```

#### Step 3: Verify Publication

```bash
# Install from PyPI
pip install deepfakebench

# Test import
python -c "import deepfakebench; print(deepfakebench.__version__)"
```

### After Publishing

Users can install with:
```bash
# Basic installation
pip install deepfakebench

# With transformers support (CLIP detectors)
pip install deepfakebench[transformers]

# Full installation
pip install deepfakebench[all]
```

### Usage After Installation

```python
# Import the package
import deepfakebench

# Use detectors
from deepfakebench.detectors import XceptionDetector

# Command-line tools
deepfakebench-train --detector_path config/detector/xception.yaml
deepfakebench-test --detector_path config/detector/xception.yaml
```

### Version Management

Update version in these files:
- `pyproject.toml`: `version = "2.0.0"`
- `setup.py`: `version='2.0.0'`
- `deepfakebench/__init__.py`: `__version__ = "2.0.0"`

### Important Notes

1. **Package Name Must Be Unique**
   - Current: `deepfakebench`
   - Alternative if taken: `deepfakebench-upgraded`, `deepfakebench2`

2. **License**: CC BY-NC 4.0 (non-commercial)
   - Ensure you have rights to publish
   - Keep original authors credited

3. **Large Files**: PyPI has 100MB limit per file
   - Don't include datasets
   - Keep pretrained weights separate

4. **Dependencies**: Specified in `requirements.txt`
   - Keep versions flexible where possible
   - Pin critical dependencies

---

## 🤝 Contributing

### How to Contribute

We welcome contributions! Here's how you can help:

1. **Report Bugs** - Open an issue with details
2. **Suggest Features** - Discuss in issues first
3. **Submit Code** - Follow the process below
4. **Improve Docs** - Fix typos, add examples
5. **Add Detectors** - Implement new detection methods

### Adding a New Detector

#### Step 1: Create Detector File

Create `deepfakebench/detectors/your_detector.py`:

```python
"""
Your Detector Implementation

Paper: [Paper Title]
Link: [Paper Link]
"""

import torch
import torch.nn as nn
from deepfakebench.detectors import DETECTOR
from deepfakebench.networks import BACKBONE


@DETECTOR.register_module(module_name='your_detector')
class YourDetector(nn.Module):
    def __init__(self, config):
        super(YourDetector, self).__init__()
        self.config = config
        
        # Load backbone
        self.backbone = BACKBONE[config['backbone_name']](
            **config['backbone_config']
        )
        
        # Add your components
        self.classifier = nn.Linear(2048, config['num_classes'])
    
    def forward(self, x):
        # Forward pass
        features = self.backbone(x)
        output = self.classifier(features)
        return output
    
    def features(self, x):
        # Feature extraction (for evaluation)
        return self.backbone(x)
```

#### Step 2: Create Configuration YAML

Create `deepfakebench/config/detector/your_detector.yaml`:

```yaml
# Model configuration
model_name: 'your_detector'
backbone_name: 'xception'
backbone_config:
  mode: 'original'
  num_classes: 2
  inc: 3
  dropout: false

# Training
pretrained: './pretrained/xception.pth'
loss_func: 'cross_entropy'
optimizer:
  adam:
    lr: 0.0002
    weight_decay: 0.0005
    beta1: 0.9
    beta2: 0.999

# Dataset
train_dataset: 'FaceForensics++'
test_dataset: 'Celeb-DF-v2'
batch_size: 32
num_workers: 4
```

#### Step 3: Register Detector

Add to `deepfakebench/detectors/__init__.py`:

```python
from .your_detector import YourDetector

__all__ = [
    # ... existing detectors ...
    'YourDetector',
]
```

#### Step 4: Add Tests

Create `tests/test_your_detector.py`:

```python
import pytest
import torch
from deepfakebench.detectors.your_detector import YourDetector

def test_detector_creation():
    config = {
        'backbone_name': 'xception',
        'backbone_config': {'num_classes': 2},
        'num_classes': 2
    }
    detector = YourDetector(config)
    assert detector is not None

def test_forward_pass():
    config = {...}
    detector = YourDetector(config)
    x = torch.randn(2, 3, 224, 224)
    output = detector(x)
    assert output.shape == (2, 2)
```

#### Step 5: Update Documentation

Add to README.md detector list and create documentation.

### Code Style Guidelines

#### Python Style
- Follow **PEP 8**
- Use **type hints** for function arguments
- Add **docstrings** to all public functions
- Keep lines under 100 characters

#### Example
```python
def preprocess_image(image: np.ndarray, size: int = 224) -> torch.Tensor:
    """
    Preprocess image for model input.
    
    Args:
        image: Input image as numpy array (H, W, C)
        size: Target size for resizing
    
    Returns:
        Preprocessed image tensor (C, H, W)
    """
    # Implementation
    pass
```

#### Imports
```python
# Standard library
import os
import sys

# Third-party
import torch
import numpy as np

# Local
from deepfakebench.detectors import DETECTOR
from deepfakebench.networks import BACKBONE
```

### Pull Request Process

1. **Fork the repository**
   ```bash
   # On GitHub, click Fork
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/DeepFakeBenchUpgraded.git
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**
   - Write code
   - Add tests
   - Update documentation

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes

### Commit Message Format

Use conventional commits:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add LSDA detector implementation
fix: correct import path in trainer.py
docs: update README with installation instructions
```

---

## 💻 Development Setup

### Local Development Environment

```bash
# 1. Clone repository
git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
cd DeepFakeBenchUpgraded

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### IDE Setup

#### VS Code

Create `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```

#### PyCharm

1. Mark `deepfakebench/` as Sources Root
2. Enable PEP 8 inspections
3. Configure interpreter to use virtual environment

### Development Tools

```bash
# Code formatting
pip install black isort

# Linting
pip install flake8 pylint

# Type checking
pip install mypy

# Testing
pip install pytest pytest-cov

# Documentation
pip install sphinx sphinx-rtd-theme
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_detectors.py

# Run with coverage
pytest tests/ --cov=deepfakebench --cov-report=html

# Run specific test function
pytest tests/test_detectors.py::test_xception_detector
```

### Writing Tests

#### Unit Tests

Test individual components:

```python
def test_backbone_output_shape():
    from deepfakebench.networks.xception import Xception
    model = Xception(num_classes=2)
    x = torch.randn(1, 3, 224, 224)
    output = model(x)
    assert output.shape == (1, 2)
```

#### Integration Tests

Test component interactions:

```python
def test_detector_training_step():
    detector = YourDetector(config)
    optimizer = torch.optim.Adam(detector.parameters())
    
    # Simulate training step
    x = torch.randn(2, 3, 224, 224)
    y = torch.tensor([0, 1])
    
    output = detector(x)
    loss = F.cross_entropy(output, y)
    loss.backward()
    optimizer.step()
    
    assert loss.item() > 0
```

### Test Coverage

Check what code is tested:

```bash
pytest --cov=deepfakebench --cov-report=term-missing
```

### Continuous Integration

Tests run automatically on GitHub Actions (if configured):

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    - name: Run tests
      run: pytest tests/
```

---

## 📚 Building Documentation

### Using Sphinx

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Initialize documentation (first time only)
cd docs
sphinx-quickstart

# Generate API documentation
sphinx-apidoc -o docs/source deepfakebench

# Build HTML documentation
cd docs
make html

# View documentation
open build/html/index.html
```

### Documentation Structure

```
docs/
├── source/
│   ├── conf.py           # Sphinx configuration
│   ├── index.rst         # Main page
│   ├── api/              # API reference
│   ├── tutorials/        # Tutorial notebooks
│   └── guides/           # User guides
└── build/
    └── html/             # Generated HTML
```

---

## 🔄 Release Process

### Creating a New Release

1. **Update version numbers**
   ```python
   # deepfakebench/__init__.py
   __version__ = "2.1.0"
   
   # pyproject.toml
   version = "2.1.0"
   
   # setup.py
   version='2.1.0'
   ```

2. **Update UPDATES.md**
   - Document all changes
   - List new features
   - Note breaking changes

3. **Run tests**
   ```bash
   pytest tests/
   ```

4. **Build package**
   ```bash
   python -m build
   ```

5. **Create git tag**
   ```bash
   git tag -a v2.1.0 -m "Release version 2.1.0"
   git push origin v2.1.0
   ```

6. **Publish to PyPI**
   ```bash
   twine upload dist/*
   ```

7. **Create GitHub Release**
   - Go to Releases on GitHub
   - Create new release from tag
   - Add release notes
   - Upload distribution files

---

## 🛠️ Automation Scripts

### Package Preparation Script

Already included: `prepare_package.sh`

```bash
#!/bin/bash
# Prepare package for distribution

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Install build tools
pip install --upgrade build twine

# Build package
python -m build

# Check distribution
twine check dist/*

echo "✓ Package prepared successfully!"
echo "To upload to TestPyPI: twine upload --repository testpypi dist/*"
echo "To upload to PyPI: twine upload dist/*"
```

### Import Path Fixer

Already included: `fix_imports.py`

```python
# Automatically fix import paths
# Usage: python fix_imports.py
```

---

## 📊 Best Practices

### Code Quality
- ✅ Write tests for new features
- ✅ Keep functions small and focused
- ✅ Use type hints
- ✅ Document complex logic
- ✅ Follow existing code style

### Performance
- ⚡ Profile before optimizing
- ⚡ Use vectorized operations
- ⚡ Leverage GPU when available
- ⚡ Cache expensive computations

### Security
- 🔒 Never commit API keys
- 🔒 Validate user inputs
- 🔒 Use `weights_only=False` cautiously
- 🔒 Keep dependencies updated

---

## 🎯 Next Steps for Developers

### Immediate Tasks
- [ ] Set up development environment
- [ ] Run existing tests
- [ ] Review code style guidelines
- [ ] Pick an issue to work on

### Learning Resources
- Read existing detector implementations
- Study the training pipeline in `trainer/`
- Explore dataset loading in `dataset/`
- Review configuration system in `config/`

### Getting Help
- Open an issue for questions
- Join discussions on GitHub
- Check existing PRs for examples
- Read the original paper

---

## 📝 Summary

### Quick Reference

| Task | Command |
|------|---------|
| Install (dev) | `pip install -e .` |
| Build package | `python -m build` |
| Run tests | `pytest tests/` |
| Format code | `black deepfakebench/` |
| Check style | `flake8 deepfakebench/` |
| Build docs | `cd docs && make html` |
| Publish | `twine upload dist/*` |

### Important Files

- `setup.py` - Package configuration
- `pyproject.toml` - Modern packaging
- `requirements.txt` - Dependencies
- `MANIFEST.in` - File inclusion rules
- `prepare_package.sh` - Build automation

### Support

- **Issues**: https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues
- **Discussions**: GitHub Discussions
- **Email**: Check repository for maintainer contact

---

**Happy Coding! 🚀**
