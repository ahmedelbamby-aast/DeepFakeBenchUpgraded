"""
DeepFakeBench Streamlit - Sidebar Component
============================================
"""

import streamlit as st
from pathlib import Path


def render_sidebar() -> str:
    """
    Render the sidebar navigation.
    
    Returns:
        Selected page name
    """
    with st.sidebar:
        # Logo and title
        st.markdown(
            """
            <div style='text-align: center; padding: 1rem 0;'>
                <h1 style='color: #1E88E5;'>🔍 DeepFakeBench</h1>
                <p style='color: #666;'>Deepfake Detection Benchmark</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### Navigation")
        
        pages = {
            "home": ("🏠", "Home"),
            "detection": ("🔎", "Detection"),
            "training": ("🎯", "Training"),
            "analysis": ("📊", "Analysis"),
            "settings": ("⚙️", "Settings"),
        }
        
        # Get current page from session state
        current_page = st.session_state.get("page", "home")
        
        for page_id, (icon, label) in pages.items():
            if st.button(
                f"{icon} {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
                type="primary" if current_page == page_id else "secondary"
            ):
                st.session_state.page = page_id
                current_page = page_id
        
        st.markdown("---")
        
        # Model status
        st.markdown("### Model Status")
        
        if st.session_state.get("current_model"):
            st.success(f"✓ Loaded: {st.session_state.current_model}")
        else:
            st.warning("⚠ No model loaded")
        
        # Device info
        try:
            import torch
            if torch.cuda.is_available():
                device_info = f"🎮 CUDA: {torch.cuda.get_device_name(0)}"
            else:
                device_info = "💻 CPU Mode"
            st.info(device_info)
        except ImportError:
            st.info("💻 PyTorch not available")
        
        st.markdown("---")
        
        # Quick links
        st.markdown("### Quick Links")
        st.markdown(
            """
            - [📖 Documentation](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded)
            - [🐛 Report Issue](https://github.com/ahmedelbamby-aast/DeepFakeBenchUpgraded/issues)
            - [📊 Original Paper](https://arxiv.org/abs/2307.01426)
            """
        )
        
        # Version info
        st.markdown("---")
        st.caption("Version 2.0.0")
    
    return current_page
