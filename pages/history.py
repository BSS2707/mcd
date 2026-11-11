"""Inspection History view with filtering, searching and deletion."""
import streamlit as st
import pandas as pd
import json
from database.db import get_all_inspections, delete_all_inspections

def render():
    st.title("📜 Inspection History & Audit Trail")
    st.markdown("Search, filter and inspect historical quality control records.")

    records = get_all_inspections()
    if not records:
        st.info("No inspection records found in the database.")
        return
        
    df = pd.DataFrame(records, columns=["ID", "Inspection ID", "Timestamp", "Image Name", "Defects", "Defect Names", "Status", "Raw Detections"])

    # Search & Filter controls
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("🔍 Search by Inspection ID or Image Name")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Pass", "Fail"])

    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Inspection ID"].str.contains(search_query, case=False) |
            filtered_df["Image Name"].str.contains(search_query, case=False)
        ]
        
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.dataframe(filtered_df[["Inspection ID", "Timestamp", "Image Name", "Defects", "Defect Names", "Status"]], use_container_width=True)

    st.markdown("---")
    if st.button("🗑️ Clear Entire History", type="secondary"):
        delete_all_inspections()
        st.success("All inspection logs cleared!")
        st.rerun()

