"""
DeepFakeBench Streamlit - Detection Page
========================================
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def get_available_models():
    """Get list of available detection models."""
    return [
        "resnet34", "efficientnetb4", "xception",
        "meso4", "meso4Inception", "f3net",
        "clip", "xclip", "timesformer", "videomae",
        "multi_attention", "srm", "recce",
        "sbi", "facexray", "spsl", "ucf", "fwa",
        "capsule_net", "core", "ffd",
        "i3d", "ftcn", "altfreezing", "stil",
        "lsda", "sladd", "pcl_xception", "iid", "lrl",
        "rfm", "uia_vit", "sia", "tall", "effort"
    ]


def render_detection():
    """Render the detection page."""
    
    st.title("🔎 Deepfake Detection")
    st.markdown("Upload an image or video to detect deepfakes.")
    
    st.markdown("---")
    
    # Model selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_model = st.selectbox(
            "Select Detection Model",
            options=get_available_models(),
            index=0,
            help="Choose a deepfake detection model"
        )
    
    with col2:
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Minimum confidence for detection"
        )
    
    st.markdown("---")
    
    # File upload
    st.markdown("### 📤 Upload Media")
    
    upload_tab, url_tab = st.tabs(["Upload File", "From URL"])
    
    with upload_tab:
        uploaded_file = st.file_uploader(
            "Choose an image or video file",
            type=["jpg", "jpeg", "png", "gif", "mp4", "avi", "mov"],
            help="Supported formats: JPG, PNG, GIF, MP4, AVI, MOV"
        )
        
        if uploaded_file is not None:
            # Display uploaded media
            file_type = uploaded_file.type
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Preview")
                if "image" in file_type:
                    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                elif "video" in file_type:
                    st.video(uploaded_file)
            
            with col2:
                st.markdown("#### File Information")
                st.info(f"""
                - **Name**: {uploaded_file.name}
                - **Type**: {file_type}
                - **Size**: {uploaded_file.size / 1024:.2f} KB
                """)
            
            # Detection button
            if st.button("🔍 Detect Deepfake", type="primary", use_container_width=True):
                with st.spinner("Analyzing media..."):
                    # Placeholder for actual detection
                    # In real implementation, this would call the detector
                    import time
                    time.sleep(2)  # Simulate processing
                    
                    # Mock results
                    is_fake = True
                    confidence = 0.87
                    
                    st.markdown("---")
                    st.markdown("### 📋 Detection Results")
                    
                    result_col1, result_col2, result_col3 = st.columns(3)
                    
                    with result_col1:
                        if is_fake:
                            st.error("⚠️ FAKE DETECTED")
                        else:
                            st.success("✓ AUTHENTIC")
                    
                    with result_col2:
                        st.metric(
                            label="Confidence",
                            value=f"{confidence * 100:.1f}%"
                        )
                    
                    with result_col3:
                        st.metric(
                            label="Model Used",
                            value=selected_model.upper()
                        )
                    
                    # Detailed results
                    with st.expander("View Detailed Analysis", expanded=True):
                        st.markdown(
                            f"""
                            **Analysis Summary:**
                            - Detection Model: {selected_model}
                            - Prediction: {'Fake' if is_fake else 'Real'}
                            - Confidence Score: {confidence:.4f}
                            - Threshold Used: {confidence_threshold}
                            
                            **Technical Details:**
                            - Processing Time: 1.23s
                            - Input Resolution: 256x256
                            - Preprocessing: Face alignment + normalization
                            """
                        )
                    
                    # Save to history
                    if "detection_results" not in st.session_state:
                        st.session_state.detection_results = []
                    
                    st.session_state.detection_results.append({
                        "file": uploaded_file.name,
                        "model": selected_model,
                        "is_fake": is_fake,
                        "confidence": confidence
                    })
    
    with url_tab:
        media_url = st.text_input(
            "Enter image or video URL",
            placeholder="https://example.com/image.jpg"
        )
        
        if media_url:
            st.info("URL-based detection coming soon!")
    
    st.markdown("---")
    
    # Detection history
    st.markdown("### 📜 Detection History")
    
    if st.session_state.get("detection_results"):
        for i, result in enumerate(reversed(st.session_state.detection_results[-5:])):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.text(result["file"])
                with col2:
                    st.text(result["model"])
                with col3:
                    if result["is_fake"]:
                        st.markdown("🔴 Fake")
                    else:
                        st.markdown("🟢 Real")
                with col4:
                    st.text(f"{result['confidence']*100:.0f}%")
    else:
        st.info("No detection history yet. Upload a file to get started!")
    
    # Tips
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown(
        """
        - **Image Quality**: Higher resolution images generally yield more accurate results
        - **Face Visibility**: Ensure faces are clearly visible and well-lit
        - **Model Selection**: Different models specialize in different types of deepfakes
        - **Confidence Threshold**: Lower threshold = more sensitive (may have false positives)
        """
    )
