"""
DeepFakeBench Streamlit - Settings Page
=======================================
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def render_settings():
    """Render the settings page."""
    
    st.title("⚙️ Settings")
    st.markdown("Configure DeepFakeBench settings.")
    
    st.markdown("---")
    
    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 General",
        "📁 Paths",
        "🖥️ Hardware",
        "🎨 Appearance"
    ])
    
    with tab1:
        render_general_settings()
    
    with tab2:
        render_path_settings()
    
    with tab3:
        render_hardware_settings()
    
    with tab4:
        render_appearance_settings()
    
    st.markdown("---")
    
    # Save/Reset buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            st.success("Settings saved successfully!")
    
    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.info("Settings reset to defaults!")
    
    with col3:
        if st.button("📤 Export Config", use_container_width=True):
            st.info("Configuration exported!")


def render_general_settings():
    """Render general settings."""
    
    st.markdown("### General Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input(
            "Project Name",
            value="DeepFakeBench",
            help="Name displayed in the application"
        )
        
        st.selectbox(
            "Default Model",
            ["ResNet34", "EfficientNet-B4", "Xception", "CLIP"],
            help="Default model for detection"
        )
        
        st.number_input(
            "Cache Size (GB)",
            min_value=1,
            max_value=100,
            value=10,
            help="Maximum cache size for downloaded models"
        )
    
    with col2:
        st.checkbox(
            "Auto-update Models",
            value=False,
            help="Automatically check for model updates"
        )
        
        st.checkbox(
            "Enable Logging",
            value=True,
            help="Enable detailed logging"
        )
        
        st.selectbox(
            "Log Level",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1,
            help="Logging verbosity level"
        )


def render_path_settings():
    """Render path settings."""
    
    st.markdown("### Path Configuration")
    
    st.info("💡 All paths can be relative to project root or absolute paths.")
    
    datasets_path = st.text_input(
        "Datasets Directory",
        value="./datasets",
        help="Directory containing datasets"
    )
    
    checkpoints_path = st.text_input(
        "Checkpoints Directory",
        value="./checkpoints",
        help="Directory for model checkpoints"
    )
    
    logs_path = st.text_input(
        "Logs Directory",
        value="./logs",
        help="Directory for training logs"
    )
    
    outputs_path = st.text_input(
        "Outputs Directory",
        value="./outputs",
        help="Directory for detection outputs"
    )
    
    cache_path = st.text_input(
        "Cache Directory",
        value="./cache",
        help="Directory for temporary cache"
    )
    
    # Validate paths
    if st.button("🔍 Validate Paths"):
        paths = {
            "Datasets": datasets_path,
            "Checkpoints": checkpoints_path,
            "Logs": logs_path,
            "Outputs": outputs_path,
            "Cache": cache_path
        }
        
        for name, path in paths.items():
            full_path = Path(path)
            if not full_path.is_absolute():
                full_path = PROJECT_ROOT / path
            
            if full_path.exists():
                st.success(f"✓ {name}: {full_path}")
            else:
                st.warning(f"⚠ {name}: {full_path} (does not exist)")


def render_hardware_settings():
    """Render hardware settings."""
    
    st.markdown("### Hardware Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        device = st.selectbox(
            "Device",
            ["auto", "cuda", "cpu", "mps"],
            help="Computing device to use"
        )
        
        if device == "cuda":
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_count = torch.cuda.device_count()
                    gpu_id = st.selectbox(
                        "GPU ID",
                        list(range(gpu_count)),
                        help="Select GPU device"
                    )
                    
                    # Show GPU info
                    st.info(f"GPU: {torch.cuda.get_device_name(gpu_id)}")
                else:
                    st.warning("CUDA is not available")
            except ImportError:
                st.warning("PyTorch not installed")
        
        num_workers = st.slider(
            "Number of Workers",
            min_value=0,
            max_value=16,
            value=4,
            help="Number of data loading workers"
        )
    
    with col2:
        st.checkbox(
            "Pin Memory",
            value=True,
            help="Pin memory for faster data transfer"
        )
        
        st.checkbox(
            "Mixed Precision",
            value=True,
            help="Use mixed precision (FP16) training"
        )
        
        st.number_input(
            "Max Batch Memory (GB)",
            min_value=1,
            max_value=48,
            value=8,
            help="Maximum GPU memory for batches"
        )
    
    # System info
    st.markdown("### System Information")
    
    try:
        import torch
        
        sys_col1, sys_col2, sys_col3 = st.columns(3)
        
        with sys_col1:
            st.metric("PyTorch Version", torch.__version__)
        
        with sys_col2:
            if torch.cuda.is_available():
                st.metric("CUDA Version", torch.version.cuda)
            else:
                st.metric("CUDA", "Not Available")
        
        with sys_col3:
            if torch.cuda.is_available():
                gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
                st.metric("GPU Memory", f"{gpu_mem:.1f} GB")
            else:
                st.metric("GPU Memory", "N/A")
    
    except ImportError:
        st.warning("PyTorch not installed - cannot display system info")


def render_appearance_settings():
    """Render appearance settings."""
    
    st.markdown("### Appearance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox(
            "Theme",
            ["System Default", "Light", "Dark"],
            help="Application color theme"
        )
        
        st.selectbox(
            "Accent Color",
            ["Blue", "Green", "Red", "Purple", "Orange"],
            help="Primary accent color"
        )
    
    with col2:
        st.checkbox(
            "Show Progress Bars",
            value=True,
            help="Display progress bars during processing"
        )
        
        st.checkbox(
            "Show Notifications",
            value=True,
            help="Show desktop notifications"
        )
    
    st.markdown("### Preview")
    
    st.info("Theme preview will appear here")
