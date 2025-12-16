"""
Streamlit Pages Module
"""

from .home import render_home
from .detection import render_detection
from .training import render_training
from .analysis import render_analysis
from .settings import render_settings

__all__ = [
    "render_home",
    "render_detection",
    "render_training",
    "render_analysis",
    "render_settings"
]
