#!/usr/bin/env python3
"""
Dataset Download Helper
=======================

Helper script to download and set up deepfake detection datasets.
"""

import os
import sys
import argparse
from pathlib import Path
import subprocess
import json

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


DATASET_INFO = {
    'faceforensics': {
        'name': 'FaceForensics++',
        'description': 'Large-scale deepfake dataset with multiple manipulation types',
        'access': 'Request access at: https://github.com/ondyari/FaceForensics',
        'size': '~1TB (full)',
        'automatic': False
    },
    'celebdf': {
        'name': 'CelebDF-v2',
        'description': 'Celebrity DeepFake dataset',
        'url': 'https://github.com/yuezunli/celeb-deepfakeforensics',
        'size': '~4GB',
        'automatic': False
    },
    'dfdc': {
        'name': 'DFDC',
        'description': 'DeepFake Detection Challenge dataset',
        'access': 'Download from Kaggle: https://www.kaggle.com/c/deepfake-detection-challenge',
        'size': '~470GB',
        'automatic': False
    },
    'uadfv': {
        'name': 'UADFV',
        'description': 'Small benchmark dataset',
        'url': 'https://github.com/danmohaha/WIFS2018_In_Ictu_Oculi',
        'size': '~2GB',
        'automatic': False
    }
}


def print_dataset_info():
    """Print information about available datasets."""
    print("\n" + "=" * 60)
    print("Available Datasets")
    print("=" * 60)
    
    for key, info in DATASET_INFO.items():
        print(f"\n{info['name']} ({key})")
        print("-" * 40)
        print(f"  Description: {info['description']}")
        print(f"  Size: {info['size']}")
        if 'url' in info:
            print(f"  URL: {info['url']}")
        if 'access' in info:
            print(f"  Access: {info['access']}")
        print(f"  Auto-download: {'Yes' if info.get('automatic') else 'No'}")


def setup_directory_structure(output_dir: Path):
    """Create directory structure for datasets."""
    directories = [
        'rgb',
        'lmdb',
        'rgb/FaceForensics++',
        'rgb/CelebDF',
        'rgb/DFDC',
        'landmarks'
    ]
    
    for dir_name in directories:
        dir_path = output_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Download and setup deepfake detection datasets'
    )
    parser.add_argument(
        '--dataset',
        choices=list(DATASET_INFO.keys()) + ['all'],
        help='Dataset to download'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./datasets',
        help='Output directory for datasets'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available datasets'
    )
    parser.add_argument(
        '--setup-dirs',
        action='store_true',
        help='Setup directory structure only'
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    
    if args.list:
        print_dataset_info()
        return
    
    if args.setup_dirs:
        print("Setting up directory structure...")
        setup_directory_structure(output_dir)
        print("\nDirectory structure created!")
        return
    
    if args.dataset:
        print(f"\nDataset: {args.dataset}")
        
        if args.dataset == 'all':
            print_dataset_info()
            print("\n⚠️  Automatic download not available for all datasets.")
            print("Please download manually from the URLs above.")
        else:
            info = DATASET_INFO.get(args.dataset)
            if info:
                print(f"\n{info['name']}")
                print(f"Description: {info['description']}")
                if 'url' in info:
                    print(f"\nDownload from: {info['url']}")
                if 'access' in info:
                    print(f"\n{info['access']}")
                
                if not info.get('automatic'):
                    print("\n⚠️  This dataset requires manual download.")
                    print("After downloading, extract to:")
                    print(f"  {output_dir}/rgb/{info['name']}/")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
