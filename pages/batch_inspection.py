"""Batch Image Inspection page."""
import streamlit as st
import uuid
import os
from models.predict import predict_image
from utils.image_processing import load_image_from_bytes, cv2_to_rgb
from database.db import add_inspection

def render():
    st.title("📦 Batch Quality Inspection")
    st.markdown("Inspect multiple motherboard images at once to automate manufacturing line review.")

    sample_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "sample_images"))
    sample_files = []
    if os.path.exists(sample_dir):
        sample_files = [f for f in os.listdir(sample_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    batch_mode = "Upload Custom Images"
    if sample_files:
        batch_mode = st.radio("Batch Source:", ["Upload Custom Images", f"Inspect All Sample Images ({len(sample_files)} found in e:/ai/sample_images)"], horizontal=True)

    items_to_process = []
    if batch_mode.startswith("Inspect All Sample Images"):
        st.write(f"Ready to process sample images: `{', '.join(sample_files)}`")
        if st.button("🚀 Run Batch Inspection on Sample Images", type="primary"):
            for sf in sample_files:
                path = os.path.join(sample_dir, sf)
                with open(path, "rb") as f:
                    items_to_process.append((sf, f.read()))
    else:
        uploaded_files = st.file_uploader("Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files and st.button("🚀 Run Batch Inspection", type="primary"):
            for f in uploaded_files:
                items_to_process.append((f.name, f.read()))

    if items_to_process:
        progress_bar = st.progress(0)
        summary = []
        
        for idx, (filename, file_bytes) in enumerate(items_to_process):
            cv2_img = load_image_from_bytes(file_bytes)
            annotated_bgr, detections = predict_image(cv2_img)
            
            defect_count = len(detections)
            status = "Fail" if defect_count > 0 else "Pass"
            defect_names = [d['name'] for d in detections]
            insp_id = f"BATCH-{uuid.uuid4().hex[:8].upper()}"
            
            add_inspection(insp_id, filename, defect_count, defect_names, detections, status)
            
            summary.append({
                "ID": insp_id,
                "File": filename,
                "Defects Found": defect_count,
                "Status": status,
                "Detected Classes": ", ".join([f"{d['name']} ({d['confidence']:.1%})" for d in detections]) if detections else "None (Defect-Free)"
            })
            
            progress_bar.progress((idx + 1) / len(items_to_process))
            
        st.success(f"Batch processing completed for {len(items_to_process)} images!")
        st.dataframe(summary, use_container_width=True)


