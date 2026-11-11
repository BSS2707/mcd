"""Live camera inspection using Streamlit camera input."""
import streamlit as st
import uuid
from models.predict import predict_image
from utils.image_processing import load_image_from_bytes, cv2_to_rgb
from database.db import add_inspection

def render():
    st.title("📷 Live Camera Visual Inspection")
    st.info("Capture a snapshot from your connected camera or industrial webcam for real-time defect localization.")

    conf_slider = st.sidebar.slider("Detection Confidence", 0.1, 1.0, 0.25, 0.05)
    
    img_file_buffer = st.camera_input("Take a motherboard photo")
    
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = load_image_from_bytes(bytes_data)
        
        with st.spinner("Processing camera capture..."):
            annotated_bgr, detections = predict_image(cv2_img, conf=conf_slider)
            
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Captured Frame")
            st.image(cv2_to_rgb(cv2_img), use_container_width=True)
        with c2:
            st.subheader("Inspection Result")
            st.image(cv2_to_rgb(annotated_bgr), use_container_width=True)
            
        defect_count = len(detections)
        status = "Fail" if defect_count > 0 else "Pass"
        defect_names = [d['name'] for d in detections]
        inspection_id = f"CAM-{uuid.uuid4().hex[:8].upper()}"

        add_inspection(
            inspection_id=inspection_id,
            image_name="Camera_Capture.png",
            defect_count=defect_count,
            defect_names=defect_names,
            detections=detections,
            status=status
        )
        
        st.success(f"Capture logged successfully as {inspection_id}!")
        if defect_count > 0:
            st.warning(f"Detected {defect_count} defect(s): {', '.join(set(defect_names))}")
        else:
            st.success("Motherboard is defect-free!")

