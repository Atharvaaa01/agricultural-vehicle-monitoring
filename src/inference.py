from ultralytics import YOLO

MODEL_PATH = "runs/detect/train10/weights/best.pt"
model = YOLO(MODEL_PATH)

# Per-class confidence thresholds
CLASS_CONF = {
    0: 0.40,  # tractor
    1: 0.40,  # truck
    2: 0.40,  # bull
    3: 0.30,  # number_plate
    4: 0.20   # sugarcane (lower because it is visually complex)
}

def detect(image):
    results = model.predict(
        source=image,
        imgsz=640,
        conf=0.15,   # global floor
        iou=0.5,
        save=False,
        verbose=False
    )

    detections = []

    for r in results:
        if r.boxes is None:
            continue

        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            # class-aware confidence filtering
            if conf < CLASS_CONF.get(cls, 0.3):
                continue

            detections.append({
                "class": cls,
                "conf": conf,
                "bbox": list(map(int, box.xyxy[0]))
            })

    return detections
