"""Dataset Information and Statistics page."""
import streamlit as st
import os
from config.settings import DATASET_DIR

def render():
    st.title("🗂️ Dataset Information & Classes")
    st.markdown("""
    This project uses the **Computer Motherboard Production Defects** dataset from Kaggle.
    
    - **Dataset URL:** [Kaggle Dataset](https://www.kaggle.com/datasets/yuelinxin/computer-motherboard-production-defects)
    - **Format:** YOLOv8 (images + txt labels)
    - **Maximum Allowed Size:** 500 MB
    """)

    st.subheader("Recognized Defect Classes (11 Total)")
    classes = [
        "1. Missing Component",
        "2. Misaligned Component",
        "3. Damaged Capacitor",
        "4. Solder Bridge / Short Circuit",
        "5. Cold / Dry Solder Joint",
        "6. Broken Trace / Scratch",
        "7. Burnt PCB Area",
        "8. Foreign Particle / Dust",
        "9. Bent Pin / Header Defect",
        "10. Discolored Solder Mask",
        "11. Solder Ball / Excess Solder"
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        for c in classes[:6]:
            st.write(f"- {c}")
    with col2:
        for c in classes[6:]:
            st.write(f"- {c}")

    st.markdown("---")
    st.subheader("Local Dataset Status")
    yaml_path = os.path.join(DATASET_DIR, "data.yaml")
    if os.path.exists(yaml_path):
        st.success(f"data.yaml found at: `{yaml_path}`")
    else:
        st.warning("data.yaml not found. Please ensure the dataset is placed into the `dataset/` directory.")

