#!/bin/bash

# DeepfakeBench Training Script
# Example usage for distributed training with multiple GPUs

# Configuration
DETECTOR="sbi"  # Change this to your detector: xception, f3net, sbi, lsda, etc.
NUM_GPUS=4      # Number of GPUs to use
BATCH_SIZE=32   # Adjust based on your GPU memory

echo "====================================="
echo "DeepfakeBench Training"
echo "====================================="
echo "Detector: ${DETECTOR}"
echo "GPUs: ${NUM_GPUS}"
echo "====================================="

# Single GPU training (recommended for testing)
# python deepfakebench/train.py --detector_path ./deepfakebench/config/detector/${DETECTOR}.yaml

# Multi-GPU training with DDP (Distributed Data Parallel)
nohup python3 -m torch.distributed.launch \
    --nproc_per_node=${NUM_GPUS} \
    deepfakebench/train.py \
    --detector_path ./deepfakebench/config/detector/${DETECTOR}.yaml \
    --ddp \
    > training_${DETECTOR}.log 2>&1 &

echo "Training started in background!"
echo "Monitor progress: tail -f training_${DETECTOR}.log"
echo "====================================="

# Additional training options:
# --no-save_ckpt     : Don't save checkpoints
# --no-save_feat     : Don't save features
# --batch_size N     : Set batch size
# --num_epochs N     : Set number of epochs