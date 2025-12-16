"""
DeepFakeBench Streamlit - Home Page
===================================
"""

import streamlit as st
from pathlib import Path


def render_home():
    """Render the home page."""
    
    # Header
    st.title("🔍 DeepFakeBench")
    st.markdown("### Comprehensive Deepfake Detection Benchmark")
    
    # Welcome message
    st.markdown(
        """
        Welcome to **DeepFakeBench**, a comprehensive benchmark for deepfake detection 
        featuring 36+ state-of-the-art detection models and support for 9+ benchmark datasets.
        """
    )
    
    st.markdown("---")
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class='stCard'>
                <h3>🔎 Detection</h3>
                <p>Upload images or videos for deepfake detection using state-of-the-art models.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Start Detection →", key="btn_detection"):
            st.session_state.page = "detection"
            st.rerun()
    
    with col2:
        st.markdown(
            """
            <div class='stCard'>
                <h3>🎯 Training</h3>
                <p>Train new detection models or fine-tune existing ones on custom datasets.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Start Training →", key="btn_training"):
            st.session_state.page = "training"
            st.rerun()
    
    with col3:
        st.markdown(
            """
            <div class='stCard'>
                <h3>📊 Analysis</h3>
                <p>Analyze model performance, compare results, and visualize metrics.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("View Analysis →", key="btn_analysis"):
            st.session_state.page = "analysis"
            st.rerun()
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📈 Platform Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric(
            label="Detection Models",
            value="36+",
            delta="Latest SOTA"
        )
    
    with stat_col2:
        st.metric(
            label="Datasets Supported",
            value="9+",
            delta="Including FF++"
        )
    
    with stat_col3:
        st.metric(
            label="PyTorch Version",
            value="2.x",
            delta="Fully Compatible"
        )
    
    with stat_col4:
        st.metric(
            label="Python Support",
            value="3.8-3.11",
            delta="Modern Python"
        )
    
    st.markdown("---")
    
    # Available models
    st.markdown("### 🤖 Available Detection Models")
    
    models = {
        "CNN-based": [
            "ResNet34", "EfficientNet-B4", "Xception", 
            "Meso4", "MesoInception4", "F3Net"
        ],
        "Transformer-based": [
            "CLIP", "X-CLIP", "TimeSformer", "VideoMAE"
        ],
        "Attention-based": [
            "Multi-Attention", "SRM", "RECCE"
        ],
        "Specialized": [
            "SBI", "Face X-Ray", "SPSL", "UCF", "FWA"
        ]
    }
    
    model_cols = st.columns(len(models))
    
    for col, (category, model_list) in zip(model_cols, models.items()):
        with col:
            st.markdown(f"**{category}**")
            for model in model_list:
                st.markdown(f"- {model}")
    
    st.markdown("---")
    
    # Quick start
    st.markdown("### 🚀 Quick Start")
    
    with st.expander("How to use this application", expanded=False):
        st.markdown(
            """
            1. **Detection Mode**: Upload an image or video to check if it's a deepfake
            2. **Training Mode**: Train a new model or fine-tune existing ones
            3. **Analysis Mode**: Compare model performances and view metrics
            
            **Getting Started:**
            ```bash
            # Install dependencies
            ./scripts/install/bash/install.sh --profile=streamlit
            
            # Run the application
            streamlit run streamlit_app/app.py
            ```
            """
        )
    
    with st.expander("System Requirements", expanded=False):
        st.markdown(
            """
            - **Python**: 3.8 - 3.11
            - **GPU**: NVIDIA GPU with CUDA support (recommended)
            - **RAM**: 8GB+ (16GB recommended for training)
            - **Storage**: 10GB+ for models and datasets
            """
        )
