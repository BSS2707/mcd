"""Dataset inspection and integrity validation script."""
import os
import glob
import yaml
from collections import Counter
from config.settings import DATASET_DIR

def inspect_dataset():
    data_yaml = os.path.join(DATASET_DIR, "data.yaml")
    if not os.path.exists(data_yaml):
        print(f"Error: {data_yaml} not found.")
        return

    with open(data_yaml, 'r') as f:
        config = yaml.safe_load(f)

    print("=== DATASET CONFIGURATION ===")
    print("Classes:", config.get('names', []))
    print("NC:", config.get('nc', 0))

    for split in ['train', 'val', 'test']:
        img_dir = os.path.join(DATASET_DIR, "images", split)
        lbl_dir = os.path.join(DATASET_DIR, "labels", split)
        
        images = glob.glob(os.path.join(img_dir, "*.*"))
        labels = glob.glob(os.path.join(lbl_dir, "*.txt"))
        
        print(f"\n--- Split: {split} ---")
        print(f"Images found: {len(images)}")
        print(f"Label files found: {len(labels)}")
        
        # Analyze class instances
        class_counter = Counter()
        for lbl_path in labels:
            with open(lbl_path, 'r') as lf:
                for line in lf:
                    parts = line.strip().split()
                    if parts:
                        class_counter[int(parts[0])] += 1
                        
        print(f"Class distribution in {split}:", dict(class_counter))

if __name__ == "__main__":
    inspect_dataset()

