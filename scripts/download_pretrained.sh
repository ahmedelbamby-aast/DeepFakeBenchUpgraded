#!/bin/bash

# ============================================================================
# Download Pretrained Models for DeepFakeBench
# ============================================================================
# This script downloads pretrained backbone weights and detector checkpoints
# from GitHub releases and places them in the correct directories.
#
# CORRECTED URLs:
# - Detector checkpoints are in v1.0.1 (not v1.0.0)
# - Extra files (landmarks, etc.) are in v1.0.2 and v1.0.0

set -e

echo "=========================================="
echo "🔽 DeepFakeBench - Download Pretrained Models"
echo "=========================================="

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Define directories
PRETRAINED_DIR="$PROJECT_ROOT/deepfakebench/pretrained"
BACKBONES_DIR="$PRETRAINED_DIR/backbones"
CHECKPOINTS_DIR="$PRETRAINED_DIR/checkpoints"
EXTRAS_DIR="$PRETRAINED_DIR/extras"

# Create directories if they don't exist
mkdir -p "$BACKBONES_DIR"
mkdir -p "$CHECKPOINTS_DIR"
mkdir -p "$EXTRAS_DIR"

# GitHub release URLs (from original DeepfakeBench)
GITHUB_RELEASE_BASE="https://github.com/SCLBD/DeepfakeBench/releases/download"

# Function to download with fallback
download_with_fallback() {
    local dest="$1"
    shift
    local urls=("$@")
    
    if [ -f "$dest" ]; then
        echo "  ✓ $(basename "$dest") already exists"
        return 0
    fi
    
    for url in "${urls[@]}"; do
        echo "  → Downloading $(basename "$dest")..."
        if wget -q --show-progress -O "$dest" "$url" 2>/dev/null; then
            echo "  ✓ Downloaded $(basename "$dest")"
            return 0
        elif curl -L -o "$dest" "$url" 2>/dev/null; then
            echo "  ✓ Downloaded $(basename "$dest")"
            return 0
        fi
    done
    
    echo "  ⚠️ Failed to download $(basename "$dest")"
    rm -f "$dest"
    return 1
}

# ============================================================================
# BACKBONE WEIGHTS
# ============================================================================
echo ""
echo "📦 Downloading Backbone Weights..."
echo "-" 

# Xception backbone (required for Xception detector)
# Try multiple sources
download_with_fallback "$PRETRAINED_DIR/xception-b5690688.pth" \
    "https://github.com/Cadene/pretrained-models.pytorch/releases/download/v1.0/xception-b5690688.pth" \
    "http://data.lip6.fr/cadene/pretrainedmodels/xception-b5690688.pth" \
    "https://data.lip6.fr/cadene/pretrainedmodels/xception-b5690688.pth"

# ResNet34 backbone
download_with_fallback "$PRETRAINED_DIR/resnet34-b627a593.pth" \
    "https://download.pytorch.org/models/resnet34-b627a593.pth"

# I3D 3D ResNet50 backbone (for video-based detectors: I3D, FTCN, AltFreezing)
download_with_fallback "$BACKBONES_DIR/I3D_8x8_R50.pth" \
    "$GITHUB_RELEASE_BASE/v1.0.3/I3D_8x8_R50.pth"

# ============================================================================
# DETECTOR CHECKPOINTS (Trained on FaceForensics++)
# CORRECTED: Use v1.0.1 which has the checkpoint files
# ============================================================================
echo ""
echo "📦 Downloading Detector Checkpoints (v1.0.1)..."
echo "-"

# URLs for detector checkpoints (from DeepfakeBench releases v1.0.1)
declare -A CHECKPOINT_URLS=(
    ["xception_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/xception_best.pth"
    ["effnb4_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/effnb4_best.pth"
    ["meso4_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/meso4_best.pth"
    ["meso4Incep_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/meso4Incep_best.pth"
    ["capsule_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/capsule_best.pth"
    ["f3net_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/f3net_best.pth"
    ["ffd_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/ffd_best.pth"
    ["srm_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/srm_best.pth"
    ["recce_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/recce_best.pth"
    ["ucf_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/ucf_best.pth"
    ["spsl_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/spsl_best.pth"
    ["core_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/core_best.pth"
    ["cnnaug_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.1/cnnaug_best.pth"
)

for checkpoint in "${!CHECKPOINT_URLS[@]}"; do
    download_with_fallback "$CHECKPOINTS_DIR/$checkpoint" "${CHECKPOINT_URLS[$checkpoint]}"
done

# ============================================================================
# EXTRA FILES (Landmarks, etc.)
# ============================================================================
echo ""
echo "📦 Downloading Extra Files..."
echo "-"

download_with_fallback "$EXTRAS_DIR/landmark_dict_ffall.pkl" \
    "$GITHUB_RELEASE_BASE/v1.0.2/landmark_dict_ffall.pkl"

download_with_fallback "$EXTRAS_DIR/nearest_face_info.pkl" \
    "$GITHUB_RELEASE_BASE/v1.0.2/nearest_face_info.pkl"

download_with_fallback "$EXTRAS_DIR/shape_predictor_81_face_landmarks.dat" \
    "$GITHUB_RELEASE_BASE/v1.0.0/shape_predictor_81_face_landmarks.dat"

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "=========================================="
echo "✅ Download Complete!"
echo "=========================================="
echo ""
echo "📁 Files downloaded to:"
echo "   • Backbones:    $PRETRAINED_DIR/"
echo "   • 3D Backbones: $BACKBONES_DIR/"
echo "   • Checkpoints:  $CHECKPOINTS_DIR/"
echo "   • Extras:       $EXTRAS_DIR/"
echo ""

# List downloaded files
echo "📋 Available backbone weights:"
ls -lh "$PRETRAINED_DIR"/*.pth 2>/dev/null | awk '{print "   • " $NF " (" $5 ")"}' || echo "   (none)"

echo ""
echo "📋 Available 3D backbone weights:"
ls -lh "$BACKBONES_DIR"/*.pth 2>/dev/null | awk '{print "   • " $NF " (" $5 ")"}' || echo "   (none)"

echo ""
echo "📋 Available detector checkpoints:"
ls -lh "$CHECKPOINTS_DIR"/*.pth 2>/dev/null | awk '{print "   • " $NF " (" $5 ")"}' || echo "   (none)"

echo ""
echo "📋 Available extra files:"
ls -lh "$EXTRAS_DIR"/* 2>/dev/null | awk '{print "   • " $NF " (" $5 ")"}' || echo "   (none)"

echo ""
echo "=========================================="
echo "🎉 Ready to train or test!"
echo "=========================================="
