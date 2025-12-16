"""
DeepFakeBench High-Level API
============================

Provides a simple, user-friendly interface for deepfake detection.

Example:
    from deepfakebench.api import Detector
    
    detector = Detector('efficientnetb4')
    result = detector.detect('path/to/image.jpg')
    print(f"Fake: {result['is_fake']}, Probability: {result['probability']:.4f}")
"""

import os
import sys
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import logging

import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F

# Add project root to path
_API_DIR = Path(__file__).resolve().parent
_PACKAGE_DIR = _API_DIR.parent
_PROJECT_ROOT = _PACKAGE_DIR.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PACKAGE_DIR))

from deepfakebench.config import get_config, PROJECT_ROOT

logger = logging.getLogger(__name__)


class DetectionError(Exception):
    """Exception raised for detection errors."""
    pass


class Detector:
    """
    High-level API for deepfake detection.
    
    Provides a simple interface for loading models and running detection
    on images and videos.
    
    Args:
        model_name: Name of the detection model (e.g., 'efficientnetb4', 'resnet34')
        config_path: Optional path to configuration file
        weights_path: Optional path to model weights
        device: Computing device ('auto', 'cuda', 'cpu', 'mps')
        
    Example:
        >>> detector = Detector('efficientnetb4')
        >>> result = detector.detect('test_image.jpg')
        >>> print(result['probability'])
        0.95
    """
    
    AVAILABLE_MODELS = [
        'resnet34', 'efficientnetb4', 'xception',
        'meso4', 'meso4Inception', 'f3net',
        'clip', 'xclip', 'timesformer', 'videomae',
        'multi_attention', 'srm', 'recce',
        'sbi', 'facexray', 'spsl', 'ucf', 'fwa',
        'capsule_net', 'core', 'ffd',
        'i3d', 'ftcn', 'altfreezing', 'stil',
        'lsda', 'sladd', 'pcl_xception', 'iid', 'lrl',
        'rfm', 'uia_vit', 'sia', 'tall', 'effort'
    ]
    
    def __init__(
        self,
        model_name: str = 'efficientnetb4',
        config_path: Optional[str] = None,
        weights_path: Optional[str] = None,
        device: str = 'auto'
    ):
        self.model_name = model_name
        self._validate_model_name(model_name)
        
        # Determine device
        self.device = self._get_device(device)
        logger.info(f"Using device: {self.device}")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize model
        self.model = None
        self._load_model(weights_path)
        
        # Preprocessing settings
        self.input_size = self.config.get('resolution', 256)
        self.normalize_mean = [0.485, 0.456, 0.406]
        self.normalize_std = [0.229, 0.224, 0.225]
    
    def _validate_model_name(self, model_name: str) -> None:
        """Validate model name."""
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(
                f"Unknown model: {model_name}. "
                f"Available models: {', '.join(self.AVAILABLE_MODELS)}"
            )
    
    def _get_device(self, device: str) -> torch.device:
        """Determine computing device."""
        if device == 'auto':
            if torch.cuda.is_available():
                return torch.device('cuda')
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return torch.device('mps')
            return torch.device('cpu')
        return torch.device(device)
    
    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load model configuration."""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = PROJECT_ROOT / 'deepfakebench' / 'config' / 'detector' / f'{self.model_name}.yaml'
        
        if config_file.exists():
            import yaml
            with open(config_file) as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded config from {config_file}")
            return config
        
        # Default config
        logger.warning(f"Config not found at {config_file}, using defaults")
        return {
            'model_name': self.model_name,
            'resolution': 256,
            'num_classes': 2
        }
    
    def _load_model(self, weights_path: Optional[str]) -> None:
        """Load detection model."""
        try:
            from deepfakebench.detectors import DETECTOR
            
            # Build model from registry
            self.model = DETECTOR.build(self.config)
            self.model = self.model.to(self.device)
            
            # Load weights if provided
            if weights_path:
                self._load_weights(weights_path)
            else:
                # Try to find pretrained weights
                pretrained_path = PROJECT_ROOT / 'deepfakebench' / 'pretrained' / f'{self.model_name}.pth'
                if pretrained_path.exists():
                    self._load_weights(str(pretrained_path))
                else:
                    logger.warning("No pretrained weights found, using random initialization")
            
            self.model.eval()
            logger.info(f"Model {self.model_name} loaded successfully")
            
        except Exception as e:
            raise DetectionError(f"Failed to load model: {e}")
    
    def _load_weights(self, weights_path: str) -> None:
        """Load model weights from checkpoint."""
        checkpoint = torch.load(weights_path, map_location=self.device, weights_only=True)
        
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        elif 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
        
        self.model.load_state_dict(state_dict, strict=False)
        logger.info(f"Loaded weights from {weights_path}")
    
    def _preprocess_image(self, image: Union[str, np.ndarray, Image.Image]) -> torch.Tensor:
        """Preprocess image for model input."""
        # Load image if path
        if isinstance(image, str):
            image = Image.open(image).convert('RGB')
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        # Resize
        image = image.resize((self.input_size, self.input_size), Image.BILINEAR)
        
        # Convert to tensor
        image_np = np.array(image).astype(np.float32) / 255.0
        
        # Normalize
        image_np = (image_np - self.normalize_mean) / self.normalize_std
        
        # Convert to tensor (C, H, W)
        tensor = torch.from_numpy(image_np).permute(2, 0, 1).float()
        
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        
        return tensor.to(self.device)
    
    @torch.no_grad()
    def detect(
        self,
        input_path: str,
        threshold: float = 0.5,
        return_features: bool = False
    ) -> Dict[str, Any]:
        """
        Detect deepfake in image.
        
        Args:
            input_path: Path to image file
            threshold: Classification threshold (0-1)
            return_features: Whether to return feature embeddings
            
        Returns:
            Dictionary containing:
                - is_fake: Boolean indicating if image is fake
                - probability: Probability of being fake (0-1)
                - confidence: Confidence score
                - features: Feature embeddings (if return_features=True)
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Image not found: {input_path}")
        
        # Preprocess
        image_tensor = self._preprocess_image(input_path)
        
        # Create data dict
        data_dict = {
            'image': image_tensor,
            'label': torch.tensor([0]).to(self.device)
        }
        
        # Forward pass
        output = self.model(data_dict, inference=True)
        
        # Extract probability
        if 'prob' in output:
            prob = output['prob'].item()
        elif 'cls' in output:
            logits = output['cls']
            prob = F.softmax(logits, dim=1)[0, 1].item()
        else:
            raise DetectionError("Model output format not recognized")
        
        result = {
            'is_fake': prob >= threshold,
            'probability': prob,
            'confidence': abs(prob - 0.5) * 2  # Scale to 0-1
        }
        
        if return_features and 'feat' in output:
            result['features'] = output['feat'].cpu().numpy()
        
        return result
    
    @torch.no_grad()
    def detect_frame(
        self,
        frame: np.ndarray,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """
        Detect deepfake in a single frame (numpy array).
        
        Args:
            frame: RGB numpy array (H, W, C)
            threshold: Classification threshold
            
        Returns:
            Detection result dictionary
        """
        # Preprocess
        image_tensor = self._preprocess_image(frame)
        
        # Create data dict
        data_dict = {
            'image': image_tensor,
            'label': torch.tensor([0]).to(self.device)
        }
        
        # Forward pass
        output = self.model(data_dict, inference=True)
        
        # Extract probability
        if 'prob' in output:
            prob = output['prob'].item()
        else:
            logits = output['cls']
            prob = F.softmax(logits, dim=1)[0, 1].item()
        
        return {
            'is_fake': prob >= threshold,
            'probability': prob,
            'confidence': abs(prob - 0.5) * 2
        }
    
    @torch.no_grad()
    def detect_batch(
        self,
        input_paths: List[str],
        threshold: float = 0.5,
        batch_size: int = 16
    ) -> List[Dict[str, Any]]:
        """
        Batch detection for multiple images.
        
        Args:
            input_paths: List of image paths
            threshold: Classification threshold
            batch_size: Processing batch size
            
        Returns:
            List of detection results
        """
        results = []
        
        for i in range(0, len(input_paths), batch_size):
            batch_paths = input_paths[i:i + batch_size]
            
            # Preprocess batch
            batch_tensors = []
            valid_indices = []
            
            for j, path in enumerate(batch_paths):
                try:
                    tensor = self._preprocess_image(path)
                    batch_tensors.append(tensor)
                    valid_indices.append(j)
                except Exception as e:
                    results.append({
                        'is_fake': None,
                        'probability': None,
                        'error': str(e)
                    })
            
            if not batch_tensors:
                continue
            
            # Stack batch
            batch_input = torch.cat(batch_tensors, dim=0)
            
            # Create data dict
            data_dict = {
                'image': batch_input,
                'label': torch.zeros(len(batch_tensors)).to(self.device)
            }
            
            # Forward pass
            output = self.model(data_dict, inference=True)
            
            # Extract probabilities
            if 'prob' in output:
                probs = output['prob'].cpu().numpy()
            else:
                logits = output['cls']
                probs = F.softmax(logits, dim=1)[:, 1].cpu().numpy()
            
            # Build results
            for j, prob in enumerate(probs):
                results.append({
                    'is_fake': prob >= threshold,
                    'probability': float(prob),
                    'confidence': float(abs(prob - 0.5) * 2)
                })
        
        return results
    
    def detect_video(
        self,
        video_path: str,
        threshold: float = 0.5,
        sample_rate: int = 10,
        max_frames: int = 100
    ) -> Dict[str, Any]:
        """
        Detect deepfake in video.
        
        Args:
            video_path: Path to video file
            threshold: Classification threshold
            sample_rate: Sample every N frames
            max_frames: Maximum frames to process
            
        Returns:
            Dictionary with overall prediction and frame-level scores
        """
        import cv2
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise DetectionError(f"Could not open video: {video_path}")
        
        frame_scores = []
        frame_count = 0
        processed_count = 0
        
        try:
            while cap.isOpened() and processed_count < max_frames:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                if frame_count % sample_rate == 0:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Detect
                    result = self.detect_frame(frame_rgb, threshold)
                    frame_scores.append(result['probability'])
                    processed_count += 1
                
                frame_count += 1
        
        finally:
            cap.release()
        
        if not frame_scores:
            raise DetectionError("No frames could be processed")
        
        # Aggregate results
        avg_prob = np.mean(frame_scores)
        
        return {
            'is_fake': avg_prob >= threshold,
            'probability': float(avg_prob),
            'confidence': float(abs(avg_prob - 0.5) * 2),
            'frame_scores': frame_scores,
            'frames_processed': processed_count,
            'aggregation': 'mean'
        }


def load_model(
    model_name: str = 'efficientnetb4',
    pretrained: bool = True,
    device: str = 'auto'
) -> Detector:
    """
    Convenience function to load a pretrained detector.
    
    Args:
        model_name: Name of the model
        pretrained: Whether to load pretrained weights
        device: Computing device
        
    Returns:
        Initialized Detector instance
    """
    weights_path = None
    if pretrained:
        weights_path = PROJECT_ROOT / 'deepfakebench' / 'pretrained' / f'{model_name}.pth'
        if not weights_path.exists():
            weights_path = None
            logger.warning(f"Pretrained weights not found for {model_name}")
    
    return Detector(
        model_name=model_name,
        weights_path=str(weights_path) if weights_path else None,
        device=device
    )


# Export
__all__ = ['Detector', 'load_model', 'DetectionError']
