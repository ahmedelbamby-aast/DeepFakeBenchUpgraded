#!/usr/bin/env python3
"""
Dataset Verification Script
===========================

Verify dataset structure and integrity.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def verify_directory_structure(dataset_dir: Path) -> dict:
    """Verify basic directory structure."""
    results = {
        'exists': dataset_dir.exists(),
        'is_directory': dataset_dir.is_dir() if dataset_dir.exists() else False,
        'subdirectories': [],
        'total_files': 0
    }
    
    if results['is_directory']:
        for item in dataset_dir.iterdir():
            if item.is_dir():
                results['subdirectories'].append(item.name)
        
        # Count files
        for f in dataset_dir.rglob('*'):
            if f.is_file():
                results['total_files'] += 1
    
    return results


def verify_frames(dataset_dir: Path, min_frames: int = 10) -> dict:
    """Verify frame images."""
    results = {
        'total_videos': 0,
        'total_frames': 0,
        'videos_with_few_frames': [],
        'empty_videos': [],
        'frame_counts': {}
    }
    
    image_extensions = {'.png', '.jpg', '.jpeg'}
    
    # Find all video directories (directories containing frame images)
    for video_dir in dataset_dir.rglob('*'):
        if not video_dir.is_dir():
            continue
        
        # Count frames in this directory
        frames = [
            f for f in video_dir.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]
        
        if frames:
            results['total_videos'] += 1
            results['total_frames'] += len(frames)
            results['frame_counts'][video_dir.name] = len(frames)
            
            if len(frames) < min_frames:
                results['videos_with_few_frames'].append({
                    'path': str(video_dir),
                    'frames': len(frames)
                })
            
            if len(frames) == 0:
                results['empty_videos'].append(str(video_dir))
    
    return results


def verify_image_integrity(dataset_dir: Path, sample_size: int = 100) -> dict:
    """Verify image file integrity (sample-based)."""
    import cv2
    
    results = {
        'checked': 0,
        'valid': 0,
        'corrupt': []
    }
    
    image_extensions = {'.png', '.jpg', '.jpeg'}
    
    # Collect all images
    all_images = [
        f for f in dataset_dir.rglob('*')
        if f.is_file() and f.suffix.lower() in image_extensions
    ]
    
    # Sample images
    import random
    sample = random.sample(all_images, min(sample_size, len(all_images)))
    
    for img_path in tqdm(sample, desc="Checking images"):
        results['checked'] += 1
        try:
            img = cv2.imread(str(img_path))
            if img is not None:
                results['valid'] += 1
            else:
                results['corrupt'].append(str(img_path))
        except Exception as e:
            results['corrupt'].append(str(img_path))
    
    return results


def verify_metadata(dataset_dir: Path, metadata_dir: Path) -> dict:
    """Verify metadata JSON files."""
    results = {
        'json_files': [],
        'total_entries': 0,
        'missing_directories': []
    }
    
    # Find JSON files
    for json_file in metadata_dir.glob('*.json'):
        results['json_files'].append(json_file.name)
        
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            # Count entries and check paths
            for dataset_name, dataset_data in data.items():
                for category, videos in dataset_data.items():
                    for video_name, video_info in videos.items():
                        results['total_entries'] += 1
                        
                        # Check if path exists
                        video_path = dataset_dir / video_info.get('path', '')
                        if not video_path.exists():
                            results['missing_directories'].append(str(video_path))
        
        except json.JSONDecodeError as e:
            results['json_files'].append(f"{json_file.name} (INVALID: {e})")
    
    return results


def print_results(results: dict, title: str):
    """Print verification results."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print('=' * 60)
    
    for key, value in results.items():
        if isinstance(value, list):
            print(f"\n{key}: ({len(value)} items)")
            if value and len(value) <= 10:
                for item in value:
                    print(f"  - {item}")
            elif value:
                for item in value[:5]:
                    print(f"  - {item}")
                print(f"  ... and {len(value) - 5} more")
        elif isinstance(value, dict):
            print(f"\n{key}: ({len(value)} items)")
            # Show summary statistics
            if value:
                values = list(value.values())
                print(f"  Min: {min(values)}, Max: {max(values)}, Avg: {sum(values)/len(values):.1f}")
        else:
            print(f"{key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description='Verify dataset structure and integrity'
    )
    parser.add_argument(
        '--dataset-dir',
        type=str,
        default='./datasets/rgb',
        help='Dataset directory to verify'
    )
    parser.add_argument(
        '--metadata-dir',
        type=str,
        default='./deepfakebench/preprocessing/dataset_json',
        help='Metadata JSON directory'
    )
    parser.add_argument(
        '--check-frames',
        action='store_true',
        help='Check frame files'
    )
    parser.add_argument(
        '--check-images',
        action='store_true',
        help='Check image integrity (sample)'
    )
    parser.add_argument(
        '--check-metadata',
        action='store_true',
        help='Check metadata JSON files'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all checks'
    )
    parser.add_argument(
        '--min-frames',
        type=int,
        default=10,
        help='Minimum frames per video (default: 10)'
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        default=100,
        help='Sample size for image integrity check (default: 100)'
    )
    
    args = parser.parse_args()
    
    dataset_dir = Path(args.dataset_dir)
    metadata_dir = Path(args.metadata_dir)
    
    print(f"Dataset Directory: {dataset_dir}")
    print(f"Metadata Directory: {metadata_dir}")
    
    # Always check directory structure
    results = verify_directory_structure(dataset_dir)
    print_results(results, "Directory Structure")
    
    if not results['exists']:
        print("\n⚠️  Dataset directory does not exist!")
        sys.exit(1)
    
    # Optional checks
    if args.check_frames or args.all:
        results = verify_frames(dataset_dir, args.min_frames)
        print_results(results, "Frame Verification")
    
    if args.check_images or args.all:
        results = verify_image_integrity(dataset_dir, args.sample_size)
        print_results(results, "Image Integrity Check")
    
    if args.check_metadata or args.all:
        results = verify_metadata(dataset_dir, metadata_dir)
        print_results(results, "Metadata Verification")
    
    print("\n" + "=" * 60)
    print("Verification Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
