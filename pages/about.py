"""About Project and Author details."""
import streamlit as st

def render():
    st.title("ℹ️ About This Project")
    st.markdown("""
    ### AI-Powered Computer Motherboard Defect Detection System
    
    This platform provides an automated visual inspection solution designed for electronics manufacturing, PCB assembly lines, and academic research.

    #### 🌟 Key Features:
    - **Real-Time YOLOv8 Detection:** Identify component misalignment, missing parts, solder defects, and shorts.
    - **Interactive Industrial UI:** Built with Streamlit, custom themed with corporate styling.
    - **Audit History:** Full SQLite-backed logging of all inspection runs.
    - **Automated QA Reports:** One-click PDF generation with ReportLab.
    - **Rich Analytics:** Interactive defect distribution and trend charts via Plotly.

    #### 👨‍💻 Project Developer:
    - **Author:** Bhavya S. Solanki
    - **Role:** Deep Learning Researcher & Full-Stack AI Engineer
    - **Frameworks:** PyTorch, Ultralytics YOLOv8, OpenCV, Streamlit, SQLite, ReportLab
    """)

