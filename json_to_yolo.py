import json
import os
from PIL import Image

JSON_FILE = "makesense_annotations.json"
IMAGE_DIR = "dataset/images/train"
LABEL_DIR = "dataset/labels/train"

os.makedirs(LABEL_DIR, exist_ok=True)

CLASSES = [
    "bullock_cart",
    "tractor",
    "truck",
    "sugarcane",
    "number_plate"
]

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# MakeSense sometimes exports a list, sometimes a dict
if isinstance(data, dict) and "annotations" in data:
    data = data["annotations"]

for item in data:
    image_name = item.get("image") or item.get("fileName")
    if image_name is None:
        continue

    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.exists(image_path):
        print(f"⚠️ Image not found: {image_name}")
        continue

    img = Image.open(image_path)
    img_w, img_h = img.size

    label_file = os.path.join(
        LABEL_DIR, os.path.splitext(image_name)[0] + ".txt"
    )

    annotations = item.get("annotations") or item.get("labels") or []

    with open(label_file, "w") as out:
        # annotations may be list OR dict
        if isinstance(annotations, dict):
            annotations = annotations.values()

        for ann in annotations:
            if not isinstance(ann, dict):
                continue

            label = ann.get("label")
            coords = ann.get("coordinates")

            if label not in CLASSES or not coords:
                continue

            class_id = CLASSES.index(label)

            x = coords["x"]
            y = coords["y"]
            w = coords["width"]
            h = coords["height"]

            x_center = (x + w / 2) / img_w
            y_center = (y + h / 2) / img_h
            w /= img_w
            h /= img_h

            out.write(
                f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n"
            )

print("✅ MakeSense JSON converted to YOLO format successfully")
