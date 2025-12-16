#!/bin/bash
# ============================================
# DeepFakeBench Installation Script
# Cross-platform Bash script for Linux/macOS
# ============================================
#
# Usage:
#   chmod +x install.sh
#   ./install.sh [OPTIONS]
#
# Options:
#   --mode=<pip|conda>      Installation mode (default: pip)
#   --cuda=<version>        CUDA version: 11.7, 11.8, 12.1, cpu (default: 11.8)
#   --profile=<profile>     Install profile: base, full, dev, streamlit (default: base)
#   --venv=<name>           Virtual environment name (default: deepfakebench-env)
#   --no-venv               Skip virtual environment creation
#   --help                  Show this help message
#
# Examples:
#   ./install.sh --mode=pip --cuda=11.8 --profile=full
#   ./install.sh --mode=conda --profile=dev
#   ./install.sh --cuda=cpu --profile=base
# ============================================

set -e  # Exit on error

# ============================================
# Configuration
# ============================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
REQUIREMENTS_DIR="$SCRIPT_DIR/../requirements"
CONDA_DIR="$SCRIPT_DIR/../conda"

# Default values
MODE="pip"
CUDA_VERSION="11.8"
PROFILE="base"
VENV_NAME="deepfakebench-env"
CREATE_VENV=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================
# Helper Functions
# ============================================
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║            DeepFakeBench Installation Script              ║"
    echo "║         Comprehensive Deepfake Detection Benchmark        ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_help() {
    head -30 "$0" | tail -20
    exit 0
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="linux";;
        Darwin*)    OS="macos";;
        CYGWIN*|MINGW*|MSYS*)    OS="windows";;
        *)          OS="unknown";;
    esac
    echo "$OS"
}

detect_gpu() {
    if check_command nvidia-smi; then
        GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
        if [ -n "$GPU_INFO" ]; then
            print_success "Detected GPU: $GPU_INFO"
            return 0
        fi
    fi
    print_warning "No NVIDIA GPU detected"
    return 1
}

# ============================================
# Parse Arguments
# ============================================
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --mode=*)
                MODE="${1#*=}"
                shift
                ;;
            --cuda=*)
                CUDA_VERSION="${1#*=}"
                shift
                ;;
            --profile=*)
                PROFILE="${1#*=}"
                shift
                ;;
            --venv=*)
                VENV_NAME="${1#*=}"
                shift
                ;;
            --no-venv)
                CREATE_VENV=false
                shift
                ;;
            --help|-h)
                show_help
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                ;;
        esac
    done
}

# ============================================
# Installation Functions
# ============================================
install_with_pip() {
    print_info "Installing with pip (profile: $PROFILE, CUDA: $CUDA_VERSION)"
    
    # Create virtual environment if requested
    if [ "$CREATE_VENV" = true ]; then
        print_info "Creating virtual environment: $VENV_NAME"
        if [ -d "$PROJECT_ROOT/$VENV_NAME" ]; then
            print_warning "Virtual environment already exists"
        else
            python -m venv "$PROJECT_ROOT/$VENV_NAME"
            print_success "Virtual environment created"
        fi
        
        # Activate virtual environment
        source "$PROJECT_ROOT/$VENV_NAME/bin/activate"
        print_success "Virtual environment activated"
    fi
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip setuptools wheel
    
    # Install PyTorch based on CUDA version
    print_info "Installing PyTorch (CUDA: $CUDA_VERSION)..."
    case $CUDA_VERSION in
        "11.7")
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
            ;;
        "11.8")
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
            ;;
        "12.1")
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
            ;;
        "cpu")
            pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
            ;;
        *)
            print_warning "Unknown CUDA version, using default PyTorch installation"
            pip install torch torchvision torchaudio
            ;;
    esac
    print_success "PyTorch installed"
    
    # Install requirements based on profile
    print_info "Installing requirements (profile: $PROFILE)..."
    case $PROFILE in
        "base")
            pip install -r "$REQUIREMENTS_DIR/requirements-base.txt"
            ;;
        "full")
            pip install -r "$REQUIREMENTS_DIR/requirements-full.txt"
            pip install git+https://github.com/openai/CLIP.git
            ;;
        "dev")
            pip install -r "$REQUIREMENTS_DIR/requirements-dev.txt"
            ;;
        "streamlit")
            pip install -r "$REQUIREMENTS_DIR/requirements-streamlit.txt"
            ;;
        "transformers")
            pip install -r "$REQUIREMENTS_DIR/requirements-transformers.txt"
            pip install git+https://github.com/openai/CLIP.git
            ;;
        *)
            print_error "Unknown profile: $PROFILE"
            exit 1
            ;;
    esac
    print_success "Requirements installed"
    
    # Install DeepFakeBench package
    print_info "Installing DeepFakeBench package..."
    pip install -e "$PROJECT_ROOT"
    print_success "DeepFakeBench installed"
}

install_with_conda() {
    print_info "Installing with Conda (profile: $PROFILE)"
    
    if ! check_command conda; then
        print_error "Conda is not installed. Please install Miniconda or Anaconda first."
        exit 1
    fi
    
    # Select environment file
    case $PROFILE in
        "base"|"full"|"dev"|"transformers")
            ENV_FILE="$CONDA_DIR/environment.yml"
            ;;
        "minimal")
            ENV_FILE="$CONDA_DIR/environment-minimal.yml"
            ;;
        "cpu")
            ENV_FILE="$CONDA_DIR/environment-cpu.yml"
            ;;
        *)
            ENV_FILE="$CONDA_DIR/environment.yml"
            ;;
    esac
    
    if [ "$CUDA_VERSION" = "cpu" ]; then
        ENV_FILE="$CONDA_DIR/environment-cpu.yml"
    fi
    
    print_info "Using environment file: $ENV_FILE"
    
    # Create conda environment
    if conda env list | grep -q "$VENV_NAME"; then
        print_warning "Conda environment '$VENV_NAME' already exists"
        print_info "Updating existing environment..."
        conda env update -n "$VENV_NAME" -f "$ENV_FILE"
    else
        conda env create -f "$ENV_FILE" -n "$VENV_NAME"
    fi
    
    print_success "Conda environment ready"
    
    # Activate and install package
    print_info "Activating conda environment..."
    eval "$(conda shell.bash hook)"
    conda activate "$VENV_NAME"
    
    # Install additional packages for non-base profiles
    if [ "$PROFILE" = "streamlit" ]; then
        pip install -r "$REQUIREMENTS_DIR/requirements-streamlit.txt"
    fi
    
    # Install DeepFakeBench package
    pip install -e "$PROJECT_ROOT"
    print_success "DeepFakeBench installed"
}

# ============================================
# Post-Installation Setup
# ============================================
setup_directories() {
    print_info "Setting up directory structure..."
    
    # Create necessary directories
    mkdir -p "$PROJECT_ROOT/datasets/rgb"
    mkdir -p "$PROJECT_ROOT/datasets/lmdb"
    mkdir -p "$PROJECT_ROOT/logs"
    mkdir -p "$PROJECT_ROOT/checkpoints"
    mkdir -p "$PROJECT_ROOT/outputs"
    mkdir -p "$PROJECT_ROOT/cache"
    
    print_success "Directory structure created"
}

create_config_template() {
    print_info "Creating configuration templates..."
    
    # Create local config if it doesn't exist
    if [ ! -f "$PROJECT_ROOT/config/local_config.yaml" ]; then
        mkdir -p "$PROJECT_ROOT/config"
        cat > "$PROJECT_ROOT/config/local_config.yaml" << 'EOF'
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
  device: auto  # auto, cuda, cpu, mps
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
EOF
        print_success "Configuration template created"
    else
        print_info "Configuration file already exists"
    fi
}

verify_installation() {
    print_info "Verifying installation..."
    
    # Check Python packages
    python -c "import torch; print(f'PyTorch: {torch.__version__}')"
    python -c "import torchvision; print(f'TorchVision: {torchvision.__version__}')"
    
    # Check CUDA if not CPU
    if [ "$CUDA_VERSION" != "cpu" ]; then
        python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
        python -c "import torch; print(f'CUDA Version: {torch.version.cuda}') if torch.cuda.is_available() else None"
    fi
    
    # Check DeepFakeBench
    python -c "import deepfakebench; print(f'DeepFakeBench: {deepfakebench.__version__}')"
    
    print_success "Installation verified"
}

# ============================================
# Main
# ============================================
main() {
    print_banner
    parse_arguments "$@"
    
    print_info "Configuration:"
    echo "  • Mode: $MODE"
    echo "  • CUDA Version: $CUDA_VERSION"
    echo "  • Profile: $PROFILE"
    echo "  • Virtual Environment: $VENV_NAME"
    echo "  • Create Venv: $CREATE_VENV"
    echo ""
    
    # Detect OS and GPU
    OS=$(detect_os)
    print_info "Detected OS: $OS"
    detect_gpu || true
    
    echo ""
    
    # Install based on mode
    case $MODE in
        "pip")
            install_with_pip
            ;;
        "conda")
            install_with_conda
            ;;
        *)
            print_error "Unknown mode: $MODE"
            exit 1
            ;;
    esac
    
    # Post-installation setup
    setup_directories
    create_config_template
    verify_installation
    
    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║              Installation Complete! 🎉                    ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Next Steps:"
    echo "  1. Activate your environment:"
    if [ "$MODE" = "conda" ]; then
        echo "     conda activate $VENV_NAME"
    else
        echo "     source $VENV_NAME/bin/activate"
    fi
    echo ""
    echo "  2. Download datasets (see docs/DATASET_GUIDE.md)"
    echo ""
    echo "  3. Download pretrained models (see docs/MODEL_GUIDE.md)"
    echo ""
    echo "  4. Start training or testing:"
    echo "     deepfakebench-train --config config/detector/resnet34.yaml"
    echo "     deepfakebench-test --config config/detector/resnet34.yaml"
    echo ""
    echo "For more information, see README.md"
}

main "$@"
