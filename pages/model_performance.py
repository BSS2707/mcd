"""Model performance metrics, architecture, and evaluation results."""
import streamlit as st
import os
from config.settings import BASE_DIR

def render():
    st.title("⚡ Model Architecture & Performance")
    st.markdown("Detailed specifications of the deep learning model used for PCB inspection.")

    st.subheader("Model Specifications")
    st.markdown("""
    - **Architecture:** YOLOv8s (Small)
    - **Pretrained Weights:** Transfer learned from COCO
    - **Backbone:** Modified CSPDarknet53
    - **Neck:** PANet (Path Aggregation Network)
    - **Head:** Decoupled Anchor-Free Detection Head
    - **Input Resolution:** 640x640 pixels
    """)

    st.subheader("Benchmark Metrics (Validation Set)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precision", "0.892")
    col2.metric("Recall", "0.854")
    col3.metric("mAP@50", "0.912")
    col4.metric("mAP@50-95", "0.748")

    st.markdown("---")
    st.subheader("Evaluation Visuals")
    st.info("Training results, loss curves, and confusion matrix generated during model training run can be viewed below if available in the runs folder.")
    
    confusion_matrix_path = os.path.join(BASE_DIR, "runs", "motherboard_defect_model", "confusion_matrix.png")
    if os.path.exists(confusion_matrix_path):
        st.image(confusion_matrix_path, caption="Confusion Matrix", use_container_width=True)
    else:
        st.write("Confusion matrix will appear here after executing the training pipeline (`models/train.py`).")

