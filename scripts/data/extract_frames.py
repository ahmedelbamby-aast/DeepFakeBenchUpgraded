#!/usr/bin/env python3
"""
Frame Extraction Script
=======================

Extract frames from video files for training/testing.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional
import cv2
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def extract_frames_from_video(
    video_path: Path,
    output_dir: Path,
    fps: int = 10,
    max_frames: Optional[int] = None,
    resize: Optional[tuple] = None
) -> int:
    """
    Extract frames from a single video.
    
    Args:
        video_path: Path to video file
        output_dir: Directory to save frames
        fps: Frames per second to extract
        max_frames: Maximum frames to extract
        resize: Optional (width, height) to resize frames
        
    Returns:
        Number of frames extracted
    """
    # Create output directory
    video_name = video_path.stem
    video_output_dir = output_dir / video_name
    video_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        print(f"Warning: Could not open {video_path}")
        return 0
    
    # Get video properties
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if video_fps <= 0:
        video_fps = 30  # Default assumption
    
    # Calculate frame interval
    frame_interval = max(1, int(video_fps / fps))
    
    frame_count = 0
    extracted_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            # Resize if specified
            if resize:
                frame = cv2.resize(frame, resize, interpolation=cv2.INTER_LINEAR)
            
            # Save frame
            frame_name = f"frame_{extracted_count:06d}.png"
            frame_path = video_output_dir / frame_name
            cv2.imwrite(str(frame_path), frame)
            
            extracted_count += 1
            
            if max_frames and extracted_count >= max_frames:
                break
        
        frame_count += 1
    
    cap.release()
    return extracted_count


def process_video_wrapper(args):
    """Wrapper for multiprocessing."""
    video_path, output_dir, fps, max_frames, resize = args
    try:
        count = extract_frames_from_video(
            video_path, output_dir, fps, max_frames, resize
        )
        return video_path.name, count, None
    except Exception as e:
        return video_path.name, 0, str(e)


def extract_frames_batch(
    input_dir: Path,
    output_dir: Path,
    fps: int = 10,
    max_frames: Optional[int] = None,
    resize: Optional[tuple] = None,
    num_workers: int = 4,
    extensions: tuple = ('.mp4', '.avi', '.mov', '.mkv')
):
    """
    Extract frames from all videos in a directory.
    """
    # Find all video files
    video_files = []
    for ext in extensions:
        video_files.extend(input_dir.rglob(f'*{ext}'))
    
    print(f"Found {len(video_files)} video files")
    
    if not video_files:
        print("No video files found!")
        return
    
    # Prepare arguments
    args_list = [
        (video_path, output_dir, fps, max_frames, resize)
        for video_path in video_files
    ]
    
    # Process with progress bar
    total_frames = 0
    errors = []
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(process_video_wrapper, args): args[0].name
            for args in args_list
        }
        
        with tqdm(total=len(video_files), desc="Extracting frames") as pbar:
            for future in as_completed(futures):
                video_name, count, error = future.result()
                total_frames += count
                if error:
                    errors.append((video_name, error))
                pbar.update(1)
    
    print(f"\nTotal frames extracted: {total_frames}")
    
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, error in errors[:10]:
            print(f"  {name}: {error}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract frames from video files'
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Input directory containing videos'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='Output directory for frames'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=10,
        help='Frames per second to extract (default: 10)'
    )
    parser.add_argument(
        '--max-frames',
        type=int,
        default=None,
        help='Maximum frames per video (default: no limit)'
    )
    parser.add_argument(
        '--resize',
        type=int,
        nargs=2,
        default=None,
        help='Resize frames to (width, height)'
    )
    parser.add_argument(
        '--num-workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    resize = tuple(args.resize) if args.resize else None
    
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"FPS: {args.fps}")
    print(f"Max frames: {args.max_frames or 'unlimited'}")
    print(f"Resize: {resize or 'original'}")
    print(f"Workers: {args.num_workers}")
    print()
    
    extract_frames_batch(
        input_dir,
        output_dir,
        fps=args.fps,
        max_frames=args.max_frames,
        resize=resize,
        num_workers=args.num_workers
    )


if __name__ == '__main__':
    main()
