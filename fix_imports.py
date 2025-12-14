#!/usr/bin/env python3
"""Fix all import paths in DeepfakeBench to use deepfakebench prefix"""

import os
import re
from pathlib import Path

def fix_imports_in_file(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Fix patterns - only if not already using deepfakebench prefix
        patterns = [
            (r'^from metrics\.registry import', 'from deepfakebench.metrics.registry import'),
            (r'^from metrics\.base_metrics_class import', 'from deepfakebench.metrics.base_metrics_class import'),
            (r'^from trainer\.', 'from deepfakebench.trainer.'),
            (r'^from networks\.', 'from deepfakebench.networks.'),
            (r'^from loss\.', 'from deepfakebench.loss.'),
            (r'^from detectors\.', 'from deepfakebench.detectors.'),
            (r'^from dataset\.', 'from deepfakebench.dataset.'),
            (r'^from detectors import', 'from deepfakebench.detectors import'),
            (r'^from networks import', 'from deepfakebench.networks import'),
            (r'^from loss import', 'from deepfakebench.loss import'),
            (r'^from trainer import', 'from deepfakebench.trainer import'),
            (r'^from dataset import', 'from deepfakebench.dataset import'),
            (r'^import metrics\.', 'import deepfakebench.metrics.'),
            (r'^import trainer\.', 'import deepfakebench.trainer.'),
            (r'^import networks\.', 'import deepfakebench.networks.'),
            (r'^import loss\.', 'import deepfakebench.loss.'),
            (r'^import detectors\.', 'import deepfakebench.detectors.'),
            (r'^import dataset\.', 'import deepfakebench.dataset.'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Fix all Python files in deepfakebench directory"""
    base_dir = Path('deepfakebench')
    if not base_dir.exists():
        print("Error: deepfakebench directory not found")
        return
    
    fixed_count = 0
    for pyfile in base_dir.rglob('*.py'):
        if fix_imports_in_file(pyfile):
            print(f"Fixed: {pyfile}")
            fixed_count += 1
    
    print(f"\n✓ Fixed {fixed_count} files")

if __name__ == '__main__':
    main()
