"""
DeepFakeBench Trainer Module
============================

Provides training utilities for deepfake detection models.
"""

import os
import sys

# Add parent directories to path for imports
current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_file_path))
project_root_dir = os.path.dirname(parent_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if project_root_dir not in sys.path:
    sys.path.append(project_root_dir)

# Import registry
from deepfakebench.metrics.registry import TRAINER

# Import Trainer class for convenience
from .trainer import Trainer

__all__ = ['TRAINER', 'Trainer']