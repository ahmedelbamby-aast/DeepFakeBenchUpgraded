# DeepFakeBench API Guide

Guide for integrating DeepFakeBench into your applications, building APIs, and using the library programmatically.

## Table of Contents

- [Python API](#python-api)
- [REST API Setup](#rest-api-setup)
- [Streamlit Integration](#streamlit-integration)
- [Custom Integration](#custom-integration)
- [Best Practices](#best-practices)

---

## Python API

### Quick Start

```python
from deepfakebench import Detector, load_model

# Load pretrained model
model = load_model('efficientnetb4', pretrained=True)

# Single image detection
result = model.detect_image('path/to/image.jpg')
print(f"Fake probability: {result['probability']:.4f}")
print(f"Prediction: {'Fake' if result['is_fake'] else 'Real'}")

# Video detection
results = model.detect_video('path/to/video.mp4')
print(f"Overall prediction: {results['prediction']}")
print(f"Frame-level scores: {results['frame_scores']}")
```

### Detector Class

```python
from deepfakebench.api import Detector

class Detector:
    """
    High-level API for deepfake detection.
    
    Args:
        model_name: Name of the detection model
        config_path: Path to configuration file (optional)
        device: Computing device ('cuda', 'cpu', 'auto')
        
    Example:
        detector = Detector('efficientnetb4', device='cuda')
        result = detector.detect('image.jpg')
    """
    
    def __init__(
        self,
        model_name: str = 'efficientnetb4',
        config_path: str = None,
        device: str = 'auto'
    ):
        pass
    
    def detect(
        self,
        input_path: str,
        threshold: float = 0.5,
        return_features: bool = False
    ) -> dict:
        """
        Detect deepfake in image or video.
        
        Args:
            input_path: Path to image or video file
            threshold: Classification threshold (0-1)
            return_features: Return feature embeddings
            
        Returns:
            Dictionary with detection results
        """
        pass
    
    def detect_batch(
        self,
        input_paths: list,
        batch_size: int = 16
    ) -> list:
        """Batch detection for multiple files."""
        pass
    
    def detect_frame(
        self,
        frame: np.ndarray,
        preprocess: bool = True
    ) -> dict:
        """Detect on single frame (numpy array)."""
        pass
```

### Configuration

```python
from deepfakebench.config import get_config, ConfigManager

# Load default configuration
config = get_config()

# Load custom configuration
config = get_config('path/to/config.yaml')

# Access configuration values
print(config.paths.datasets)
print(config.hardware.device)
print(config['model_name'])

# Modify configuration
config['batch_size'] = 64
config.hardware.num_workers = 8

# Save configuration
config.save('my_config.yaml')
```

---

## REST API Setup

### FastAPI Implementation

Create `api/server.py`:

```python
"""
DeepFakeBench REST API Server
=============================

Run with: uvicorn api.server:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import tempfile
import os
import sys
from pathlib import Path

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from deepfakebench.api import Detector

# Initialize app
app = FastAPI(
    title="DeepFakeBench API",
    description="REST API for deepfake detection",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global detector instance
detector: Optional[Detector] = None


# Models
class DetectionResult(BaseModel):
    """Detection result schema."""
    filename: str
    is_fake: bool
    probability: float
    confidence: float
    model_used: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    cuda_available: bool


class ModelInfo(BaseModel):
    """Model information."""
    name: str
    description: str
    parameters: int
    supported_inputs: List[str]


# Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize detector on startup."""
    global detector
    try:
        detector = Detector(model_name='efficientnetb4', device='auto')
        print("Detector initialized successfully")
    except Exception as e:
        print(f"Failed to initialize detector: {e}")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    import torch
    return HealthResponse(
        status="healthy",
        model_loaded=detector is not None,
        cuda_available=torch.cuda.is_available()
    )


@app.get("/models", response_model=List[str])
async def list_models():
    """List available detection models."""
    return [
        "resnet34", "efficientnetb4", "xception",
        "meso4", "meso4Inception", "f3net",
        "clip", "xclip", "timesformer", "videomae",
        "sbi", "facexray", "spsl", "ucf", "fwa"
    ]


@app.get("/models/{model_name}", response_model=ModelInfo)
async def get_model_info(model_name: str):
    """Get information about a specific model."""
    model_info = {
        "efficientnetb4": ModelInfo(
            name="EfficientNet-B4",
            description="Efficient CNN-based detector with high accuracy",
            parameters=19300000,
            supported_inputs=["image", "video"]
        ),
        "resnet34": ModelInfo(
            name="ResNet-34",
            description="Fast and reliable CNN-based detector",
            parameters=21800000,
            supported_inputs=["image", "video"]
        )
    }
    
    if model_name not in model_info:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return model_info[model_name]


@app.post("/detect/image", response_model=DetectionResult)
async def detect_image(
    file: UploadFile = File(...),
    threshold: float = 0.5
):
    """
    Detect deepfake in uploaded image.
    
    Args:
        file: Image file (JPEG, PNG)
        threshold: Classification threshold (0-1)
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {allowed_types}"
        )
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Run detection
        result = detector.detect(tmp_path, threshold=threshold)
        
        return DetectionResult(
            filename=file.filename,
            is_fake=result['is_fake'],
            probability=result['probability'],
            confidence=result.get('confidence', result['probability']),
            model_used=detector.model_name
        )
    finally:
        # Cleanup
        os.unlink(tmp_path)


@app.post("/detect/video", response_model=DetectionResult)
async def detect_video(
    file: UploadFile = File(...),
    threshold: float = 0.5,
    sample_rate: int = 10
):
    """
    Detect deepfake in uploaded video.
    
    Args:
        file: Video file (MP4, AVI)
        threshold: Classification threshold (0-1)
        sample_rate: Sample every N frames
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    allowed_types = ['video/mp4', 'video/avi', 'video/quicktime']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {allowed_types}"
        )
    
    # Save to temp file
    suffix = '.mp4' if 'mp4' in file.content_type else '.avi'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # Run detection
        result = detector.detect_video(
            tmp_path,
            threshold=threshold,
            sample_rate=sample_rate
        )
        
        return DetectionResult(
            filename=file.filename,
            is_fake=result['is_fake'],
            probability=result['probability'],
            confidence=result.get('confidence', result['probability']),
            model_used=detector.model_name
        )
    finally:
        # Cleanup
        os.unlink(tmp_path)


@app.post("/detect/batch")
async def detect_batch(files: List[UploadFile] = File(...)):
    """Batch detection for multiple files."""
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for file in files:
        try:
            result = await detect_image(file)
            results.append(result)
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return results


@app.post("/model/load")
async def load_model(model_name: str):
    """Load a different detection model."""
    global detector
    
    try:
        detector = Detector(model_name=model_name, device='auto')
        return {"status": "success", "model": model_name}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to load model: {str(e)}"
        )


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run the API Server

```bash
# Install dependencies
pip install fastapi uvicorn python-multipart

# Run server
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload

# Or with custom settings
uvicorn api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Usage Examples

```bash
# Health check
curl http://localhost:8000/health

# List models
curl http://localhost:8000/models

# Detect image
curl -X POST "http://localhost:8000/detect/image" \
    -H "accept: application/json" \
    -F "file=@test_image.jpg"

# Detect video
curl -X POST "http://localhost:8000/detect/video" \
    -H "accept: application/json" \
    -F "file=@test_video.mp4"

# Load different model
curl -X POST "http://localhost:8000/model/load?model_name=xception"
```

### Python Client

```python
import requests

class DeepFakeBenchClient:
    """Python client for DeepFakeBench API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def detect_image(self, image_path: str, threshold: float = 0.5) -> dict:
        """Detect deepfake in image."""
        with open(image_path, 'rb') as f:
            files = {'file': f}
            params = {'threshold': threshold}
            response = requests.post(
                f"{self.base_url}/detect/image",
                files=files,
                params=params
            )
        return response.json()
    
    def detect_video(self, video_path: str) -> dict:
        """Detect deepfake in video."""
        with open(video_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/detect/video",
                files=files
            )
        return response.json()

# Usage
client = DeepFakeBenchClient()
result = client.detect_image('test.jpg')
print(result)
```

---

## Streamlit Integration

### Basic Integration

```python
import streamlit as st
from deepfakebench.api import Detector

# Cache the detector
@st.cache_resource
def load_detector(model_name: str):
    return Detector(model_name=model_name)

# App
st.title("DeepFake Detector")

model = st.selectbox("Model", ["efficientnetb4", "resnet34", "xception"])
detector = load_detector(model)

uploaded = st.file_uploader("Upload image", type=['jpg', 'png'])

if uploaded:
    # Display image
    st.image(uploaded, caption="Uploaded Image")
    
    # Save and detect
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
        tmp.write(uploaded.getvalue())
        result = detector.detect(tmp.name)
    
    # Show results
    if result['is_fake']:
        st.error(f"⚠️ FAKE DETECTED ({result['probability']:.1%})")
    else:
        st.success(f"✓ REAL ({1-result['probability']:.1%})")
```

### Run Streamlit App

```bash
# Run the full Streamlit application
streamlit run streamlit_app/app.py

# With custom port
streamlit run streamlit_app/app.py --server.port 8501
```

---

## Custom Integration

### Embedding in Existing Applications

```python
from deepfakebench.api import Detector
import numpy as np
from PIL import Image

class MyApplication:
    def __init__(self):
        # Initialize detector
        self.detector = Detector(
            model_name='efficientnetb4',
            device='cuda'
        )
    
    def process_frame(self, frame: np.ndarray) -> dict:
        """Process a single video frame."""
        # frame should be RGB numpy array (H, W, C)
        return self.detector.detect_frame(frame)
    
    def process_stream(self, stream):
        """Process video stream."""
        for frame in stream:
            result = self.process_frame(frame)
            yield result
```

### Async Support

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncDetector:
    def __init__(self, model_name: str = 'efficientnetb4'):
        self.detector = Detector(model_name)
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def detect_async(self, image_path: str) -> dict:
        """Async detection."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.detector.detect,
            image_path
        )
    
    async def detect_batch_async(self, paths: list) -> list:
        """Async batch detection."""
        tasks = [self.detect_async(p) for p in paths]
        return await asyncio.gather(*tasks)

# Usage
async def main():
    detector = AsyncDetector()
    result = await detector.detect_async('image.jpg')
    print(result)

asyncio.run(main())
```

---

## Best Practices

### 1. Model Loading

```python
# DO: Load model once, reuse for multiple detections
detector = Detector('efficientnetb4')
for image in images:
    result = detector.detect(image)

# DON'T: Load model for each detection
for image in images:
    detector = Detector('efficientnetb4')  # Slow!
    result = detector.detect(image)
```

### 2. Batch Processing

```python
# DO: Use batch processing for multiple images
results = detector.detect_batch(images, batch_size=32)

# DON'T: Process one at a time
results = [detector.detect(img) for img in images]  # Slower
```

### 3. GPU Memory Management

```python
import torch

# Clear GPU cache periodically
torch.cuda.empty_cache()

# Use mixed precision for memory efficiency
detector = Detector('efficientnetb4', mixed_precision=True)

# Process in smaller batches if OOM
detector.detect_batch(images, batch_size=8)  # Reduce if needed
```

### 4. Error Handling

```python
from deepfakebench.api import Detector, DetectionError

try:
    result = detector.detect('image.jpg')
except FileNotFoundError:
    print("Image file not found")
except DetectionError as e:
    print(f"Detection failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 5. Production Deployment

```python
# Use environment variables for configuration
import os

config = {
    'model_name': os.getenv('DETECTOR_MODEL', 'efficientnetb4'),
    'device': os.getenv('DETECTOR_DEVICE', 'auto'),
    'threshold': float(os.getenv('DETECTOR_THRESHOLD', '0.5'))
}

detector = Detector(**config)
```

---

## Next Steps

- [Training Guide](TRAINING_GUIDE.md) - Train custom models
- [Model Guide](MODEL_GUIDE.md) - Add new models
- [Dataset Guide](DATASET_GUIDE.md) - Prepare datasets
