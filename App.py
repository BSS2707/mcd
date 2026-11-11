"""Main Streamlit Application Coordinator.

Runs the multi-page motherboard defect detection dashboard.
"""
import streamlit as st
from database.db import init_db
from config.settings import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR

# Page configuration
st.set_page_config(
    page_title="AI Motherboard Defect Inspection",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
init_db()

# Custom Industrial Styling
st.markdown(f"""
    <style>
    .main {{
        background-color: #F8F9FA;
    }}
    .sidebar .sidebar-content {{
        background-color: {PRIMARY_COLOR};
    }}
    h1, h2, h3 {{
        color: {PRIMARY_COLOR};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-radius: 6px;
        border: none;
    }}
    .stButton>button:hover {{
        background-color: {SECONDARY_COLOR};
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/integrated-circuit.png", width=70)
st.sidebar.title("QC Navigation")
st.sidebar.markdown("**System Version:** `v1.0.0`")
st.sidebar.markdown(f"<span style='color:{ACCENT_COLOR}; font-weight:bold;'>Motherboard AI Inspector</span>", unsafe_allow_html=True)

pages = {
    "📊 Dashboard": "dashboard",
    "🔬 Single Image Inspection": "image_inspection",
    "📷 Live Camera": "live_camera",
    "📦 Batch Inspection": "batch_inspection",
    "📜 Inspection History": "history",
    "📈 Quality Analytics": "analytics",
    "📑 PDF Reports": "pdf_reports",
    "⚡ Model Performance": "model_performance",
    "🗂️ Dataset Information": "dataset_info",
    "ℹ️ About Project": "about"
}

selection = st.sidebar.radio("Select Module:", list(pages.keys()))
page_key = pages[selection]

# Modular Page Dispatcher
if page_key == "dashboard":
    from pages.dashboard import render
    render()
elif page_key == "image_inspection":
    from pages.image_inspection import render
    render()
elif page_key == "live_camera":
    from pages.live_camera import render
    render()
elif page_key == "batch_inspection":
    from pages.batch_inspection import render
    render()
elif page_key == "history":
    from pages.history import render
    render()
elif page_key == "analytics":
    from pages.analytics import render
    render()
elif page_key == "pdf_reports":
    from pages.pdf_reports import render
    render()
elif page_key == "model_performance":
    from pages.model_performance import render
    render()
elif page_key == "dataset_info":
    from pages.dataset_info import render
    render()
elif page_key == "about":
    from pages.about import render
    render()

