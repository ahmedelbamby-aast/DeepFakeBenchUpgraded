"""
DeepFakeBench Streamlit Application
====================================

A modern web interface for deepfake detection using Streamlit.

Usage:
    streamlit run app.py
    
    Or with custom settings:
    streamlit run app.py --server.port 8501 --server.address localhost
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from deepfakebench.config import get_config
from pages.home import render_home
from pages.detection import render_detection
from pages.training import render_training
from pages.analysis import render_analysis
from pages.settings import render_settings
from components.sidebar import render_sidebar


# Page configuration
st.set_page_config(
    page_title="DeepFakeBench",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded",
        "Report a bug": "https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues",
        "About": "DeepFakeBench: Comprehensive Deepfake Detection Benchmark"
    }
)

# Custom CSS
def load_css():
    """Load custom CSS styles."""
    st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Header styles */
    .stTitle {
        color: #1E88E5;
    }
    
    /* Card-like containers */
    .stCard {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Metric display */
    .metric-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1E88E5;
    }
    
    /* Upload area */
    .uploadedFile {
        border: 2px dashed #1E88E5;
        border-radius: 10px;
        padding: 2rem;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #1E88E5;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
    }
    
    .stButton > button:hover {
        border-color: #1E88E5;
        color: #1E88E5;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f1f3f4;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 1rem;
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "config" not in st.session_state:
        st.session_state.config = get_config()
    
    if "current_model" not in st.session_state:
        st.session_state.current_model = None
    
    if "detection_results" not in st.session_state:
        st.session_state.detection_results = []
    
    if "page" not in st.session_state:
        st.session_state.page = "home"


def main():
    """Main application entry point."""
    # Load CSS
    load_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render selected page
    if page == "home":
        render_home()
    elif page == "detection":
        render_detection()
    elif page == "training":
        render_training()
    elif page == "analysis":
        render_analysis()
    elif page == "settings":
        render_settings()
    else:
        render_home()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888;'>
            DeepFakeBench v2.0 | 
            <a href='https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded'>GitHub</a> |
            Made with ❤️
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
