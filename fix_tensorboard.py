#!/usr/bin/env python3
"""
Fix TensorBoard imports to be optional - wrap in try/except blocks
This allows the package to work even if tensorboard is not installed
"""

import os
import re
from pathlib import Path

def fix_tensorboard_imports(file_path):
    """Make tensorboard imports optional with try/except"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file imports SummaryWriter
    if 'from torch.utils.tensorboard import SummaryWriter' not in content:
        return False
    
    # Pattern to find the import line
    pattern = r'^from torch\.utils\.tensorboard import SummaryWriter$'
    
    # Check if already wrapped in try/except
    if 'try:' in content and 'torch.utils.tensorboard' in content:
        print(f"  Already fixed: {file_path}")
        return False
    
    # Replace with try/except wrapped version
    replacement = '''try:
    from torch.utils.tensorboard import SummaryWriter
    TENSORBOARD_AVAILABLE = True
except ImportError:
    SummaryWriter = None
    TENSORBOARD_AVAILABLE = False'''
    
    # Replace the import
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    # Find all Python files in deepfakebench directory
    root_dir = Path('deepfakebench')
    files_fixed = 0
    
    print("Fixing TensorBoard imports to be optional...")
    print("=" * 70)
    
    for py_file in root_dir.rglob('*.py'):
        if fix_tensorboard_imports(py_file):
            print(f"✓ Fixed: {py_file}")
            files_fixed += 1
    
    print("=" * 70)
    print(f"Fixed {files_fixed} files")
    print("TensorBoard is now optional - package will work without it!")

if __name__ == '__main__':
    main()
