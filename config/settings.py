"""Configuration settings for the Motherboard Defect Detection System.

All paths are relative to the project root (e:\ai\motherboard_defect_detection).
"""
import os

# ---------- Project Paths ----------
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_DIR = os.path.join(DATASET_DIR, "labels")
MODEL_DIR = os.path.join(BASE_DIR, "models")
DB_PATH = os.path.join(BASE_DIR, "database", "inspections.db")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# ---------- UI Colours ----------
PRIMARY_COLOR = "#253C6D"
SECONDARY_COLOR = "#30497D"
ACCENT_COLOR = "#F2842F"
STEEL_BLUE = "#455B8A"

# ---------- Model Settings ----------
YOLO_MODEL_NAME = "yolov8s.pt"  # default pretrained model
TRAIN_EPOCHS = 50
BATCH_SIZE = 16
IMG_SIZE = 640

# ---------- Misc ----------
MAX_DATASET_SIZE_MB = 500

