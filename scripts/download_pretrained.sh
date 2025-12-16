#!/bin/bash

# ============================================================================
# Download Pretrained Models for DeepFakeBench
# ============================================================================
# This script downloads pretrained backbone weights and detector checkpoints
# from GitHub releases and places them in the correct directories.

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

# Create directories if they don't exist
mkdir -p "$BACKBONES_DIR"
mkdir -p "$CHECKPOINTS_DIR"

# GitHub release URLs (from original DeepfakeBench)
GITHUB_RELEASE_BASE="https://github.com/SCLBD/DeepfakeBench/releases/download"

# ============================================================================
# BACKBONE WEIGHTS
# ============================================================================
echo ""
echo "📦 Downloading Backbone Weights..."
echo "-" 

# Xception backbone (required for Xception detector)
XCEPTION_URL="https://github.com/Cadene/pretrained-models.pytorch/releases/download/v1.0/xception-b5690688.pth"
XCEPTION_FILE="$PRETRAINED_DIR/xception-b5690688.pth"
if [ ! -f "$XCEPTION_FILE" ]; then
    echo "  → Downloading Xception backbone..."
    wget -q --show-progress -O "$XCEPTION_FILE" "$XCEPTION_URL" 2>/dev/null || \
    curl -L -o "$XCEPTION_FILE" "$XCEPTION_URL" 2>/dev/null || \
    echo "  ⚠️ Failed to download Xception backbone"
else
    echo "  ✓ Xception backbone already exists"
fi

# ResNet34 backbone
RESNET34_URL="https://download.pytorch.org/models/resnet34-b627a593.pth"
RESNET34_FILE="$PRETRAINED_DIR/resnet34-b627a593.pth"
if [ ! -f "$RESNET34_FILE" ]; then
    echo "  → Downloading ResNet34 backbone..."
    wget -q --show-progress -O "$RESNET34_FILE" "$RESNET34_URL" 2>/dev/null || \
    curl -L -o "$RESNET34_FILE" "$RESNET34_URL" 2>/dev/null || \
    echo "  ⚠️ Failed to download ResNet34 backbone"
else
    echo "  ✓ ResNet34 backbone already exists"
fi

# I3D 3D ResNet50 backbone (for video-based detectors: I3D, FTCN, AltFreezing)
I3D_URL="$GITHUB_RELEASE_BASE/v1.0.3/I3D_8x8_R50.pth"
I3D_FILE="$BACKBONES_DIR/I3D_8x8_R50.pth"
if [ ! -f "$I3D_FILE" ]; then
    echo "  → Downloading I3D 3D R50 backbone (for video detectors)..."
    wget -q --show-progress -O "$I3D_FILE" "$I3D_URL" 2>/dev/null || \
    curl -L -o "$I3D_FILE" "$I3D_URL" 2>/dev/null || \
    echo "  ⚠️ Failed to download I3D backbone"
else
    echo "  ✓ I3D 3D R50 backbone already exists"
fi

# HRNet backbone (optional, for some detectors)
HRNET_URL="https://github.com/HRNet/HRNet-Image-Classification/releases/download/PretrainedWeights/hrnetv2_w48_imagenet_pretrained.pth"
HRNET_FILE="$PRETRAINED_DIR/hrnetv2_w48_imagenet_pretrained.pth"
if [ ! -f "$HRNET_FILE" ]; then
    echo "  → Downloading HRNet backbone (optional)..."
    wget -q --show-progress -O "$HRNET_FILE" "$HRNET_URL" 2>/dev/null || \
    curl -L -o "$HRNET_FILE" "$HRNET_URL" 2>/dev/null || \
    echo "  ⚠️ Failed to download HRNet backbone (optional)"
else
    echo "  ✓ HRNet backbone already exists"
fi

# ============================================================================
# DETECTOR CHECKPOINTS (Trained on FaceForensics++)
# ============================================================================
echo ""
echo "📦 Downloading Detector Checkpoints..."
echo "-"

# URLs for detector checkpoints (from DeepfakeBench releases)
declare -A CHECKPOINT_URLS=(
    ["xception_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/xception_best.pth"
    ["effnb4_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/effnb4_best.pth"
    ["meso4_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/meso4_best.pth"
    ["meso4Incep_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/meso4Incep_best.pth"
    ["capsule_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/capsule_best.pth"
    ["f3net_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/f3net_best.pth"
    ["ffd_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/ffd_best.pth"
    ["srm_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/srm_best.pth"
    ["recce_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/recce_best.pth"
    ["ucf_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/ucf_best.pth"
    ["spsl_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/spsl_best.pth"
    ["core_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/core_best.pth"
    ["cnnaug_best.pth"]="$GITHUB_RELEASE_BASE/v1.0.0/cnnaug_best.pth"
)

for checkpoint in "${!CHECKPOINT_URLS[@]}"; do
    CHECKPOINT_FILE="$CHECKPOINTS_DIR/$checkpoint"
    if [ ! -f "$CHECKPOINT_FILE" ]; then
        echo "  → Downloading $checkpoint..."
        wget -q --show-progress -O "$CHECKPOINT_FILE" "${CHECKPOINT_URLS[$checkpoint]}" 2>/dev/null || \
        curl -L -o "$CHECKPOINT_FILE" "${CHECKPOINT_URLS[$checkpoint]}" 2>/dev/null || \
        echo "  ⚠️ Failed to download $checkpoint"
    else
        echo "  ✓ $checkpoint already exists"
    fi
done

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "=========================================="
echo "✅ Download Complete!"
echo "=========================================="
echo ""
echo "📁 Files downloaded to:"
echo "   • Backbones:   $PRETRAINED_DIR/"
echo "   • 3D Backbones: $BACKBONES_DIR/"
echo "   • Checkpoints: $CHECKPOINTS_DIR/"
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
echo "=========================================="
echo "🎉 Ready to train or test!"
echo "=========================================="
