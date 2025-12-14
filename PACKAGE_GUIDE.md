# Quick Reference: Converting DeepfakeBench to Pip Package

## 🎯 Summary

Transform your DeepfakeBench project into an installable Python package that users can install with `pip install deepfakebench`.

## 📋 Quick Steps

### 1. **Prepare Files** (5 min)

Already created for you:
- ✅ `setup.py` - Package configuration
- ✅ `pyproject.toml` - Modern Python packaging
- ✅ `MANIFEST.in` - File inclusion rules
- ✅ `requirements.txt` - Dependencies
- ✅ `README.md` - Package documentation

### 2. **Restructure Code** (10 min)

```bash
# Rename main directory
mv training deepfakebench

# Keep backup
cp -r training training_backup
```

### 3. **Build Package** (2 min)

```bash
# Run preparation script
bash prepare_package.sh

# Or manually:
pip install build twine
python -m build
```

### 4. **Test Locally** (5 min)

```bash
# Install locally
pip install dist/deepfakebench-2.0.0-py3-none-any.whl

# Test import
python -c "from deepfakebench.detectors import XceptionDetector; print('✓ Works!')"
```

### 5. **Publish** (5 min)

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Then publish to PyPI
twine upload dist/*
```

## 🚀 After Publishing

Users install with:
```bash
pip install deepfakebench
```

Use in code:
```python
from deepfakebench.detectors import XceptionDetector
```

## 📦 Files You Created

| File | Purpose |
|------|---------|
| `setup.py` | Classic packaging config |
| `pyproject.toml` | Modern PEP 517/518 config |
| `MANIFEST.in` | Include/exclude files |
| `prepare_package.sh` | Automation script |
| `PYPI_PUBLISHING.md` | Detailed guide |

## ⚙️ What Changes

### Before (Repository):
```
deepfakebench/
  detectors/
  networks/
  dataset/
```

Usage:
```python
sys.path.insert(0, 'deepfakebench')
from detectors.xception_detector import XceptionDetector
```

### After (Package):
```
deepfakebench/
  detectors/
  networks/
  dataset/
```

Usage:
```python
from deepfakebench.detectors import XceptionDetector
```

## ✅ Checklist

- [ ] Run `prepare_package.sh`
- [ ] Test local install
- [ ] Test imports work
- [ ] Upload to TestPyPI
- [ ] Test from TestPyPI
- [ ] Upload to PyPI
- [ ] Update README with pip install instructions

## 💡 Tips

1. **Choose unique name**: Check https://pypi.org first
2. **Version properly**: Use semantic versioning (2.0.0)
3. **Test thoroughly**: TestPyPI is your friend
4. **Document well**: Good README = more users
5. **Keep license**: CC BY-NC 4.0 (credit original authors)

## 📚 Resources

- Full guide: `PYPI_PUBLISHING.md`
- PyPI: https://pypi.org
- TestPyPI: https://test.pypi.org
- Packaging guide: https://packaging.python.org

---

**Need help?** See `PYPI_PUBLISHING.md` for detailed instructions!
