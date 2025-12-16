"""
DeepfakeBench: A Comprehensive Benchmark of Deepfake Detection
Upgraded for PyTorch 2.x and Python 3.8+ compatibility

Original authors: Zhiyuan Yan, Yong Zhang, Xinhang Yuan, Siwei Lyu, Baoyuan Wu
Upgraded by: Ahmed ElBamby
"""

__version__ = "2.0.0"
__author__ = "Zhiyuan Yan, Ahmed ElBamby"
__description__ = "Comprehensive Deepfake Detection Benchmark"

# Import main modules
try:
    from . import detectors
    from . import networks
    from . import dataset
    from . import trainer
    from . import config
    from .api import Detector, load_model
    __all__ = [
        'detectors', 'networks', 'dataset', 'trainer', 
        'config', 'Detector', 'load_model', '__version__'
    ]
except ImportError:
    # Allow package to be imported even if submodules have issues
    __all__ = ['__version__']
