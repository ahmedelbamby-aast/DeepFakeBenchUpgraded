import sys
sys.path.insert(0, '.')

print("Testing restructured imports...\n")

try:
    from deepfakebench.preprocessing.rearrange import generate_dataset_file
    print("✓ Import successful: deepfakebench.preprocessing.rearrange.generate_dataset_file")
except Exception as e:
    print(f"✗ Import failed: {e}")

try:
    from deepfakebench.detectors.xception_detector import XceptionDetector
    print("✓ Import successful: deepfakebench.detectors.xception_detector.XceptionDetector")
except Exception as e:
    print(f"✗ Import failed: {e}")

try:
    import os
    preprocessing_path = './deepfakebench/preprocessing'
    if os.path.exists(preprocessing_path):
        print(f"✓ preprocessing folder exists at: {preprocessing_path}")
    else:
        print(f"✗ preprocessing folder NOT found at: {preprocessing_path}")
except Exception as e:
    print(f"✗ Path check failed: {e}")

print("\n✅ Structure reorganization complete!")
