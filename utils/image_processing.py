"""Image processing utilities for motherboard defect detection."""
import cv2
import numpy as np
from PIL import Image
import io

def load_image_from_bytes(image_bytes):
    """Loads an image from raw bytes to OpenCV BGR format."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def cv2_to_bytes(cv2_img):
    """Converts an OpenCV BGR image to JPEG bytes."""
    success, encoded_img = cv2.imencode('.jpg', cv2_img)
    if success:
        return encoded_img.tobytes()
    return None

def cv2_to_rgb(cv2_img):
    """Converts OpenCV BGR image to RGB format for PIL / Streamlit display."""
    return cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

def draw_detections(image, detections, box_color=(47, 132, 242), text_color=(255, 255, 255)):
    """
    Draws custom bounding boxes and labels onto the image.
    detections: list of dicts [{'name': ..., 'confidence': ..., 'box': [x1, y1, x2, y2]}]
    box_color: BGR tuple (default accent color #F2842F -> BGR (47, 132, 242))
    """
    img_copy = image.copy()
    for det in detections:
        box = det.get('box', [])
        if len(box) == 4:
            x1, y1, x2, y2 = [int(v) for v in box]
            label = f"{det['name']} {det['confidence']:.2f}"
            
            # Draw box
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), box_color, 2)
            
            # Label background
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(img_copy, (x1, max(0, y1 - 20)), (x1 + w, y1), box_color, -1)
            cv2.putText(img_copy, label, (x1, max(15, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
            
    return img_copy

