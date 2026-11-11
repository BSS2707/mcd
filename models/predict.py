"""Inference wrapper for YOLOv8 Motherboard Defect Detection."""
import os
import cv2
import numpy as np
from ultralytics import YOLO
from config.settings import MODEL_DIR

_model_instance = None

def get_model(model_path=None):
    """Loads and caches the YOLOv8 model."""
    global _model_instance
    if _model_instance is not None:
        return _model_instance

    if model_path is None:
        # Check custom trained model first, fallback to local yolov8s.pt in project root
        best_pt = os.path.join(MODEL_DIR, "best.pt")
        local_yolo = os.path.join(os.path.dirname(MODEL_DIR), "yolov8s.pt")
        if os.path.exists(best_pt):
            model_path = best_pt
        elif os.path.exists(local_yolo):
            model_path = local_yolo
        else:
            model_path = "yolov8s.pt"

    _model_instance = YOLO(model_path)
    return _model_instance

def predict_image(image_input, conf=0.25, iou=0.45, model_path=None):
    """
    Performs inference on an image.
    image_input: np.ndarray (OpenCV BGR) or path string.
    Returns:
      annotated_image: np.ndarray (BGR)
      detections: list of dicts [{'name': ..., 'confidence': ..., 'box': [x1, y1, x2, y2], 'class_id': ...}]
    """
    model = get_model(model_path)
    results = model.predict(source=image_input, conf=conf, iou=iou, verbose=False)
    
    detections = []
    annotated_img = None
    
    if len(results) > 0:
        res = results[0]
        annotated_img = res.plot()  # Ultralytics pre-rendered BGR image
        
        boxes = res.boxes
        if boxes is not None:
            for b in boxes:
                xyxy = b.xyxy[0].tolist()
                conf_val = float(b.conf[0])
                cls_id = int(b.cls[0])
                cls_name = model.names.get(cls_id, str(cls_id))
                detections.append({
                    'class_id': cls_id,
                    'name': cls_name,
                    'confidence': conf_val,
                    'box': xyxy
                })
    else:
        annotated_img = image_input if isinstance(image_input, np.ndarray) else cv2.imread(image_input)

    return annotated_img, detections

