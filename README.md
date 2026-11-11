# AI-Powered Computer Motherboard Defect Detection System

**Author / Developer:** Bhavya S. Solanki  
**Platform:** Industrial Quality-Control Vision Suite  
**Core Technologies:** Python, PyTorch, Ultralytics YOLOv8, OpenCV, Streamlit, SQLite, Plotly, ReportLab

---

## 📌 Project Overview
An end-to-end computer vision and deep learning inspection platform for printed circuit boards (PCBs) and computer motherboards. The system classifies, detects, and localizes 11 categories of manufacturing defects using transfer-learned YOLOv8 models, delivering automated inspection logging and PDF quality reports.

---

## 🗂️ Directory Structure

```
motherboard_defect_detection/
├── App.py                    # Streamlit Application Coordinator
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── .gitignore                # Git ignore rules
│
├── config/
│   ├── __init__.py
│   └── settings.py           # Paths, styling colors, hyperparameters
│
├── database/
│   ├── __init__.py
│   └── db.py                 # SQLite database transactions
│
├── models/
│   ├── __init__.py
│   ├── train.py              # YOLOv8 training and validation routines
│   └── predict.py            # Model inference caching and defect detection
│
├── pages/                    # 10 UI Module Views
│   ├── __init__.py
│   ├── dashboard.py          # KPI metrics & quick charts
│   ├── image_inspection.py   # Single image deep learning analysis
│   ├── live_camera.py        # Snapshot webcam inspection
│   ├── batch_inspection.py   # Bulk multi-image processing
│   ├── history.py            # SQLite audit trail & search
│   ├── analytics.py          # Plotly distribution and time trends
│   ├── pdf_reports.py        # ReportLab compliance report generation
│   ├── model_performance.py  # Precision, Recall, mAP evaluation
│   ├── dataset_info.py       # Kaggle dataset specs & defect classes
│   └── about.py              # Project developer info
│
├── utils/
│   ├── __init__.py
│   ├── image_processing.py   # OpenCV conversion & drawing
│   ├── analytics.py          # Plotly figures & pandas queries
│   ├── report_generator.py   # PDF generation engine
│   └── dataset_analysis.py   # Dataset distribution analyzer
│
├── dataset/                  # Kaggle YOLOv8 dataset destination
│   ├── images/
│   ├── labels/
│   └── data.yaml
│
├── reports/                  # Generated PDF reports storage
└── runs/                     # YOLOv8 training output checkpoints
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
```bash
streamlit run App.py
```

### 3. Training on Kaggle Dataset
1. Download dataset from [Kaggle](https://www.kaggle.com/datasets/yuelinxin/computer-motherboard-production-defects).
2. Extract files into the `dataset/` directory ensuring `data.yaml` exists.
3. Validate dataset integrity:
   ```bash
   python utils/dataset_analysis.py
   ```
4. Run training:
   ```bash
   python models/train.py --epochs 50 --batch 16 --imgsz 640
   ```

