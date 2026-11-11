"""YOLOv8 training and validation script for Motherboard Defect Detection."""
import os
import argparse
from ultralytics import YOLO
from config.settings import BASE_DIR, DATASET_DIR, TRAIN_EPOCHS, BATCH_SIZE, IMG_SIZE

def train_model(data_yaml=None, epochs=TRAIN_EPOCHS, batch=BATCH_SIZE, imgsz=IMG_SIZE, model_name="yolov8s.pt"):
    """
    Trains YOLOv8 on the motherboard defects dataset.
    """
    if data_yaml is None:
        data_yaml = os.path.join(DATASET_DIR, "data.yaml")

    if not os.path.exists(data_yaml):
        raise FileNotFoundError(f"data.yaml not found at {data_yaml}. Please download the Kaggle dataset first.")

    model = YOLO(model_name)
    print(f"Starting training: model={model_name}, data={data_yaml}, epochs={epochs}, batch={batch}, imgsz={imgsz}")
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        project=os.path.join(BASE_DIR, "runs"),
        name="motherboard_defect_model",
        save=True
    )
    return results

def validate_model(weights_path=None, data_yaml=None):
    """
    Validates a trained model.
    """
    if weights_path is None:
        weights_path = os.path.join(BASE_DIR, "models", "best.pt")
    if data_yaml is None:
        data_yaml = os.path.join(DATASET_DIR, "data.yaml")

    model = YOLO(weights_path)
    metrics = model.val(data=data_yaml)
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Motherboard Defect Detection YOLOv8 model")
    parser.add_argument("--epochs", type=int, default=TRAIN_EPOCHS)
    parser.add_argument("--batch", type=int, default=BATCH_SIZE)
    parser.add_argument("--imgsz", type=int, default=IMG_SIZE)
    parser.add_argument("--model", type=str, default="yolov8s.pt")
    args = parser.parse_args()

    train_model(epochs=args.epochs, batch=args.batch, imgsz=args.imgsz, model_name=args.model)

