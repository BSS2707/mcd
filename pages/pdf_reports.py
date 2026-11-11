"""PDF Reports Download & Generation page."""
import streamlit as st
import json
from database.db import get_all_inspections
from utils.report_generator import generate_pdf_report

def render():
    st.title("📑 Quality Inspection Reports")
    st.markdown("Generate and download formal compliance and QA inspection reports.")

    records = get_all_inspections()
    if not records:
        st.info("No inspection records available to create reports.")
        return

    options = {f"{r[1]} ({r[3]} - {r[6]})": r for r in records}
    selected_label = st.selectbox("Select an Inspection Record:", list(options.keys()))

    if selected_label:
        rec = options[selected_label]
        # Columns: id, inspection_id, timestamp, image_name, defect_count, defect_names, status, detections_json
        insp_data = {
            "inspection_id": rec[1],
            "timestamp": rec[2],
            "image_name": rec[3],
            "defect_count": rec[4],
            "defect_names": rec[5],
            "status": rec[6],
            "detections": json.loads(rec[7]) if rec[7] else []
        }

        if st.button("Generate & Download PDF", type="primary"):
            with st.spinner("Generating ReportLab PDF document..."):
                pdf_path = generate_pdf_report(insp_data)
                
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Click here to download PDF",
                    data=f.read(),
                    file_name=f"Report_{insp_data['inspection_id']}.pdf",
                    mime="application/pdf"
                )

