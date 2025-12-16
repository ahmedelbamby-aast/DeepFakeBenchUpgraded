# ============================================
# DeepFakeBench Installation Script
# PowerShell script for Windows
# ============================================
#
# Usage:
#   .\install.ps1 [OPTIONS]
#
# Options:
#   -Mode <pip|conda>       Installation mode (default: pip)
#   -CudaVersion <version>  CUDA version: 11.7, 11.8, 12.1, cpu (default: 11.8)
#   -Profile <profile>      Install profile: base, full, dev, streamlit (default: base)
#   -VenvName <name>        Virtual environment name (default: deepfakebench-env)
#   -NoVenv                 Skip virtual environment creation
#   -Help                   Show this help message
#
# Examples:
#   .\install.ps1 -Mode pip -CudaVersion 11.8 -Profile full
#   .\install.ps1 -Mode conda -Profile dev
#   .\install.ps1 -CudaVersion cpu -Profile base
# ============================================

param(
    [ValidateSet("pip", "conda")]
    [string]$Mode = "pip",
    
    [ValidateSet("11.7", "11.8", "12.1", "cpu")]
    [string]$CudaVersion = "11.8",
    
    [ValidateSet("base", "full", "dev", "streamlit", "transformers", "minimal")]
    [string]$Profile = "base",
    
    [string]$VenvName = "deepfakebench-env",
    
    [switch]$NoVenv,
    
    [switch]$Help
)

# ============================================
# Configuration
# ============================================
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Item $ScriptDir).Parent.Parent.Parent.FullName
$RequirementsDir = Join-Path $ScriptDir "..\requirements"
$CondaDir = Join-Path $ScriptDir "..\conda"

# ============================================
# Helper Functions
# ============================================
function Write-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║            DeepFakeBench Installation Script              ║" -ForegroundColor Cyan
    Write-Host "║         Comprehensive Deepfake Detection Benchmark        ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

function Show-Help {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Test-GPU {
    try {
        $gpuInfo = & nvidia-smi --query-gpu=name --format=csv,noheader 2>$null | Select-Object -First 1
        if ($gpuInfo) {
            Write-Success "Detected GPU: $gpuInfo"
            return $true
        }
    }
    catch {
        # GPU not found
    }
    Write-Warning-Custom "No NVIDIA GPU detected"
    return $false
}

# ============================================
# Installation Functions
# ============================================
function Install-WithPip {
    Write-Info "Installing with pip (profile: $Profile, CUDA: $CudaVersion)"
    
    # Create virtual environment if requested
    if (-not $NoVenv) {
        $VenvPath = Join-Path $ProjectRoot $VenvName
        
        Write-Info "Creating virtual environment: $VenvName"
        if (Test-Path $VenvPath) {
            Write-Warning-Custom "Virtual environment already exists"
        }
        else {
            python -m venv $VenvPath
            Write-Success "Virtual environment created"
        }
        
        # Activate virtual environment
        $ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
        & $ActivateScript
        Write-Success "Virtual environment activated"
    }
    
    # Upgrade pip
    Write-Info "Upgrading pip..."
    python -m pip install --upgrade pip setuptools wheel
    
    # Install PyTorch based on CUDA version
    Write-Info "Installing PyTorch (CUDA: $CudaVersion)..."
    switch ($CudaVersion) {
        "11.7" {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
        }
        "11.8" {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        }
        "12.1" {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        }
        "cpu" {
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        }
        default {
            Write-Warning-Custom "Unknown CUDA version, using default PyTorch installation"
            pip install torch torchvision torchaudio
        }
    }
    Write-Success "PyTorch installed"
    
    # Install requirements based on profile
    Write-Info "Installing requirements (profile: $Profile)..."
    switch ($Profile) {
        "base" {
            pip install -r (Join-Path $RequirementsDir "requirements-base.txt")
        }
        "full" {
            pip install -r (Join-Path $RequirementsDir "requirements-full.txt")
            pip install git+https://github.com/openai/CLIP.git
        }
        "dev" {
            pip install -r (Join-Path $RequirementsDir "requirements-dev.txt")
        }
        "streamlit" {
            pip install -r (Join-Path $RequirementsDir "requirements-streamlit.txt")
        }
        "transformers" {
            pip install -r (Join-Path $RequirementsDir "requirements-transformers.txt")
            pip install git+https://github.com/openai/CLIP.git
        }
        default {
            Write-Error-Custom "Unknown profile: $Profile"
            exit 1
        }
    }
    Write-Success "Requirements installed"
    
    # Install DeepFakeBench package
    Write-Info "Installing DeepFakeBench package..."
    pip install -e $ProjectRoot
    Write-Success "DeepFakeBench installed"
}

function Install-WithConda {
    Write-Info "Installing with Conda (profile: $Profile)"
    
    if (-not (Test-Command "conda")) {
        Write-Error-Custom "Conda is not installed. Please install Miniconda or Anaconda first."
        exit 1
    }
    
    # Select environment file
    switch ($Profile) {
        "minimal" {
            $EnvFile = Join-Path $CondaDir "environment-minimal.yml"
        }
        "cpu" {
            $EnvFile = Join-Path $CondaDir "environment-cpu.yml"
        }
        default {
            $EnvFile = Join-Path $CondaDir "environment.yml"
        }
    }
    
    if ($CudaVersion -eq "cpu") {
        $EnvFile = Join-Path $CondaDir "environment-cpu.yml"
    }
    
    Write-Info "Using environment file: $EnvFile"
    
    # Check if environment exists
    $EnvExists = conda env list | Select-String -Pattern "^$VenvName\s"
    
    if ($EnvExists) {
        Write-Warning-Custom "Conda environment '$VenvName' already exists"
        Write-Info "Updating existing environment..."
        conda env update -n $VenvName -f $EnvFile
    }
    else {
        conda env create -f $EnvFile -n $VenvName
    }
    
    Write-Success "Conda environment ready"
    
    # Activate and install package
    Write-Info "To activate the conda environment, run:"
    Write-Host "  conda activate $VenvName" -ForegroundColor Yellow
    
    # Install DeepFakeBench package
    conda activate $VenvName
    pip install -e $ProjectRoot
    Write-Success "DeepFakeBench installed"
}

# ============================================
# Post-Installation Setup
# ============================================
function Setup-Directories {
    Write-Info "Setting up directory structure..."
    
    # Create necessary directories
    $Directories = @(
        "datasets\rgb",
        "datasets\lmdb",
        "logs",
        "checkpoints",
        "outputs",
        "cache"
    )
    
    foreach ($Dir in $Directories) {
        $FullPath = Join-Path $ProjectRoot $Dir
        if (-not (Test-Path $FullPath)) {
            New-Item -ItemType Directory -Path $FullPath -Force | Out-Null
        }
    }
    
    Write-Success "Directory structure created"
}

function Create-ConfigTemplate {
    Write-Info "Creating configuration templates..."
    
    $ConfigPath = Join-Path $ProjectRoot "config\local_config.yaml"
    
    if (-not (Test-Path $ConfigPath)) {
        $ConfigDir = Join-Path $ProjectRoot "config"
        if (-not (Test-Path $ConfigDir)) {
            New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
        }
        
        $ConfigContent = @"
# ============================================
# DeepFakeBench Local Configuration
# ============================================
# This file contains local settings that override defaults
# Copy this file and modify as needed

# Paths (use absolute paths or relative to project root)
paths:
  datasets: ./datasets
  rgb_dir: ./datasets/rgb
  lmdb_dir: ./datasets/lmdb
  checkpoints: ./checkpoints
  logs: ./logs
  outputs: ./outputs
  cache: ./cache

# Hardware settings
hardware:
  device: auto  # auto, cuda, cpu
  num_workers: 4
  pin_memory: true

# Training defaults
training:
  batch_size: 32
  learning_rate: 0.0002
  epochs: 50
  save_frequency: 5
  log_frequency: 100

# Inference defaults
inference:
  batch_size: 64
  save_predictions: true
"@
        $ConfigContent | Out-File -FilePath $ConfigPath -Encoding UTF8
        Write-Success "Configuration template created"
    }
    else {
        Write-Info "Configuration file already exists"
    }
}

function Test-Installation {
    Write-Info "Verifying installation..."
    
    try {
        # Check Python packages
        python -c "import torch; print(f'PyTorch: {torch.__version__}')"
        python -c "import torchvision; print(f'TorchVision: {torchvision.__version__}')"
        
        # Check CUDA if not CPU
        if ($CudaVersion -ne "cpu") {
            python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
            python -c "import torch; print(f'CUDA Version: {torch.version.cuda}') if torch.cuda.is_available() else None"
        }
        
        # Check DeepFakeBench
        python -c "import deepfakebench; print(f'DeepFakeBench: {deepfakebench.__version__}')"
        
        Write-Success "Installation verified"
    }
    catch {
        Write-Error-Custom "Installation verification failed: $_"
    }
}

# ============================================
# Main
# ============================================
function Main {
    if ($Help) {
        Show-Help
    }
    
    Write-Banner
    
    Write-Info "Configuration:"
    Write-Host "  • Mode: $Mode"
    Write-Host "  • CUDA Version: $CudaVersion"
    Write-Host "  • Profile: $Profile"
    Write-Host "  • Virtual Environment: $VenvName"
    Write-Host "  • Create Venv: $(-not $NoVenv)"
    Write-Host ""
    
    # Detect GPU
    $null = Test-GPU
    Write-Host ""
    
    # Install based on mode
    switch ($Mode) {
        "pip" {
            Install-WithPip
        }
        "conda" {
            Install-WithConda
        }
        default {
            Write-Error-Custom "Unknown mode: $Mode"
            exit 1
        }
    }
    
    # Post-installation setup
    Setup-Directories
    Create-ConfigTemplate
    Test-Installation
    
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              Installation Complete! 🎉                    ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:"
    Write-Host "  1. Activate your environment:" -ForegroundColor White
    if ($Mode -eq "conda") {
        Write-Host "     conda activate $VenvName" -ForegroundColor Yellow
    }
    else {
        Write-Host "     .\$VenvName\Scripts\Activate.ps1" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "  2. Download datasets (see docs\DATASET_GUIDE.md)" -ForegroundColor White
    Write-Host ""
    Write-Host "  3. Download pretrained models (see docs\MODEL_GUIDE.md)" -ForegroundColor White
    Write-Host ""
    Write-Host "  4. Start training or testing:" -ForegroundColor White
    Write-Host "     deepfakebench-train --config config\detector\resnet34.yaml" -ForegroundColor Yellow
    Write-Host "     deepfakebench-test --config config\detector\resnet34.yaml" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "For more information, see README.md"
}

Main
