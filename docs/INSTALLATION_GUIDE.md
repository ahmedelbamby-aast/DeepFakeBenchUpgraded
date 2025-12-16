# DeepFakeBench Installation Guide

Complete installation guide for DeepFakeBench - supporting Windows, Linux, and macOS.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Using Pip (Recommended)](#using-pip-recommended)
  - [Using Conda](#using-conda)
  - [Using Docker](#using-docker)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Installation Profiles](#installation-profiles)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Linux/macOS (Bash)

```bash
# Clone the repository
git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
cd DeepFakeBenchUpgraded

# Run installation script
chmod +x scripts/install/bash/install.sh
./scripts/install/bash/install.sh --mode=pip --cuda=11.8 --profile=full
```

### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded.git
cd DeepFakeBenchUpgraded

# Run installation script
.\scripts\install\powershell\install.ps1 -Mode pip -CudaVersion 11.8 -Profile full
```

---

## Prerequisites

### Required

- **Python**: 3.8, 3.9, 3.10, or 3.11
- **Git**: For cloning the repository
- **pip** or **Conda**: Package manager

### Recommended

- **NVIDIA GPU**: CUDA-capable GPU with at least 8GB VRAM
- **CUDA Toolkit**: 11.7, 11.8, or 12.1
- **cuDNN**: Compatible with your CUDA version
- **RAM**: 16GB or more
- **Storage**: 50GB+ for datasets and models

### Check Your Environment

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check CUDA (if using GPU)
nvidia-smi
nvcc --version
```

---

## Installation Methods

### Using Pip (Recommended)

#### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv deepfakebench-env

# Activate (Linux/macOS)
source deepfakebench-env/bin/activate

# Activate (Windows)
.\deepfakebench-env\Scripts\Activate.ps1
```

#### Step 2: Install PyTorch

Choose the appropriate command based on your CUDA version:

```bash
# CUDA 11.8 (Recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CPU only
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### Step 3: Install Requirements

```bash
# Base installation
pip install -r scripts/install/requirements/requirements-base.txt

# Or full installation with all features
pip install -r scripts/install/requirements/requirements-full.txt
```

#### Step 4: Install DeepFakeBench

```bash
# Install in editable mode
pip install -e .
```

---

### Using Conda

#### Step 1: Create Environment

```bash
# Full environment with GPU support
conda env create -f scripts/install/conda/environment.yml

# CPU-only environment
conda env create -f scripts/install/conda/environment-cpu.yml

# Minimal environment (inference only)
conda env create -f scripts/install/conda/environment-minimal.yml
```

#### Step 2: Activate Environment

```bash
conda activate deepfakebench
```

#### Step 3: Install DeepFakeBench

```bash
pip install -e .
```

---

### Using Docker

```bash
# Build Docker image
docker build -t deepfakebench:latest .

# Run container with GPU support
docker run --gpus all -it -v $(pwd)/datasets:/app/datasets deepfakebench:latest

# Run container without GPU
docker run -it -v $(pwd)/datasets:/app/datasets deepfakebench:latest
```

---

## Platform-Specific Instructions

### Windows

1. **Enable Long Paths** (recommended):
   ```powershell
   # Run as Administrator
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
       -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```

2. **Install Visual C++ Build Tools** (if needed):
   - Download from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"

3. **Run Installation**:
   ```powershell
   # With execution policy override
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   .\scripts\install\powershell\install.ps1 -Mode pip -Profile full
   ```

### Linux (Ubuntu/Debian)

1. **Install System Dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y python3-dev python3-pip python3-venv \
       build-essential cmake git libgl1-mesa-glx libglib2.0-0
   ```

2. **Run Installation**:
   ```bash
   ./scripts/install/bash/install.sh --mode=pip --profile=full
   ```

### macOS

1. **Install Homebrew** (if not installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Dependencies**:
   ```bash
   brew install python cmake
   ```

3. **Run Installation**:
   ```bash
   ./scripts/install/bash/install.sh --mode=pip --cuda=cpu --profile=full
   ```

   Note: macOS with Apple Silicon uses MPS (Metal Performance Shaders) instead of CUDA.

---

## Installation Profiles

| Profile | Description | Use Case |
|---------|-------------|----------|
| `base` | Core dependencies only | Basic detection/training |
| `full` | All dependencies including transformers | Full feature set |
| `dev` | Development tools (testing, linting) | Development/contribution |
| `streamlit` | Web interface dependencies | Running Streamlit app |
| `transformers` | CLIP/X-CLIP model support | Transformer-based detectors |

### Profile Selection

```bash
# Bash
./scripts/install/bash/install.sh --profile=<profile>

# PowerShell
.\scripts\install\powershell\install.ps1 -Profile <profile>
```

---

## Troubleshooting

### Common Issues

#### 1. CUDA Version Mismatch

```
RuntimeError: The detected CUDA version (...) mismatches the version that was used to compile PyTorch
```

**Solution**: Install PyTorch with matching CUDA version:
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu<VERSION>
```

#### 2. Out of Memory (OOM)

```
CUDA out of memory
```

**Solutions**:
- Reduce batch size in configuration
- Use mixed precision training (`--mixed_precision`)
- Use gradient accumulation
- Use a model with fewer parameters

#### 3. OpenCV Import Error

```
ImportError: libGL.so.1: cannot open shared object file
```

**Solution (Linux)**:
```bash
sudo apt install libgl1-mesa-glx libglib2.0-0
```

#### 4. Tokenizers Build Error

```
error: can't find Rust compiler
```

**Solution**:
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Or use pre-built wheel
pip install tokenizers --prefer-binary
```

#### 5. DLib Installation Error

**Solution**: DLib is optional. If installation fails, skip it:
```bash
pip install -r requirements-base.txt
# Ignore dlib errors
```

### Verify Installation

```bash
# Run verification script
python -c "
import torch
import deepfakebench

print(f'DeepFakeBench: {deepfakebench.__version__}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA Available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA Version: {torch.version.cuda}')
    print(f'GPU: {torch.cuda.get_device_name(0)}')
"
```

### Getting Help

- **GitHub Issues**: [Report a bug](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues)
- **Documentation**: [Full docs](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/tree/main/docs)
- **Discord/Slack**: [Community](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded)

---

## Next Steps

After installation:

1. **Download Datasets**: See [Dataset Guide](DATASET_GUIDE.md)
2. **Download Models**: See [Model Guide](MODEL_GUIDE.md)
3. **Start Training**: See [Training Guide](TRAINING_GUIDE.md)
4. **Run Detection**: See [Detection Guide](DETECTION_GUIDE.md)
