"""Single Image Inspection page."""
import streamlit as st
import uuid
import os
import cv2
from models.predict import predict_image
from utils.image_processing import load_image_from_bytes, cv2_to_rgb, cv2_to_bytes
from database.db import add_inspection
from utils.report_generator import generate_pdf_report
from config.settings import REPORTS_DIR

def render():
    st.title("🔬 Single Image Defect Inspection")
    st.markdown("Upload a motherboard or PCB high-resolution image to perform deep-learning defect identification.")

    conf_slider = st.sidebar.slider("Confidence Threshold", min_value=0.1, max_value=1.0, value=0.25, step=0.05)
    iou_slider = st.sidebar.slider("IOU Threshold", min_value=0.1, max_value=1.0, value=0.45, step=0.05)

    # Sample Images Shortcut
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "sample_images"))
    sample_files = []
    if os.path.exists(sample_dir):
        sample_files = [f for f in os.listdir(sample_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    input_mode = "Upload an Image"
    if sample_files:
        input_mode = st.radio("Select Image Source:", ["Upload an Image", "Choose from Sample Images (e:/ai/sample_images)"], horizontal=True)

    cv2_img = None
    image_name = None

    if input_mode == "Choose from Sample Images (e:/ai/sample_images)":
        selected_sample = st.selectbox("Select a sample motherboard image:", sample_files)
        if selected_sample:
            sample_path = os.path.join(sample_dir, selected_sample)
            with open(sample_path, "rb") as f:
                file_bytes = f.read()
            cv2_img = load_image_from_bytes(file_bytes)
            image_name = selected_sample
    else:
        uploaded_file = st.file_uploader("Choose an image (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            cv2_img = load_image_from_bytes(file_bytes)
            image_name = uploaded_file.name

    if cv2_img is not None:
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(cv2_to_rgb(cv2_img), use_container_width=True)
            
        if st.button("🚀 Run AI Inspection", type="primary"):
            with st.spinner("Analyzing circuitry with YOLOv8..."):
                annotated_bgr, detections = predict_image(cv2_img, conf=conf_slider, iou=iou_slider)
                
            with col2:
                st.subheader("AI Detection Result")
                st.image(cv2_to_rgb(annotated_bgr), use_container_width=True)

            defect_count = len(detections)
            status = "Fail" if defect_count > 0 else "Pass"
            defect_names = [d['name'] for d in detections]
            inspection_id = f"INSP-{uuid.uuid4().hex[:8].upper()}"

            # Save to Database
            add_inspection(
                inspection_id=inspection_id,
                image_name=image_name,
                defect_count=defect_count,
                defect_names=defect_names,
                detections=detections,
                status=status
            )
            
            st.success(f"Inspection complete! Inspection ID: `{inspection_id}`")
            
            # Display Metrics
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Status", status)
            mcol2.metric("Defects Found", defect_count)
            mcol3.metric("Unique Classes", len(set(defect_names)))
            
            if defect_count > 0:
                st.markdown("### Detected Defects List")
                det_table = [{
                    "Class": d['name'],
                    "Confidence": f"{d['confidence']:.2%}",
                    "Box (X1, Y1, X2, Y2)": [round(x, 1) for x in d['box']]
                } for d in detections]
                st.table(det_table)
                
            # Quick PDF Export
            annotated_tmp_path = os.path.join(REPORTS_DIR, f"temp_{inspection_id}.jpg")
            os.makedirs(REPORTS_DIR, exist_ok=True)
            cv2.imwrite(annotated_tmp_path, annotated_bgr)
            
            insp_data = {
                "inspection_id": inspection_id,
                "timestamp": "Just now",
                "image_name": image_name,
                "defect_count": defect_count,
                "detections": detections,
                "status": status
            }
            pdf_path = generate_pdf_report(insp_data, annotated_img_path=annotated_tmp_path)
            
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Inspection PDF Report",
                    data=f.read(),
                    file_name=f"{inspection_id}_report.pdf",
                    mime="application/pdf"
                )

