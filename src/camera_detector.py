import os
os.environ["ULTRALYTICS_DISABLE_CV2_IMSHOW"] = "1"

import cv2
from src.inference import detect
from src.ocr_processor import extract_text
from src.plate_color_detector import detect_color

CLASS_NAMES = {
    0: "Tractor",
    1: "Truck",
    2: "Bull",
    3: "Number Plate",
    4: "Sugarcane"
}

def run_camera(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError("Camera not accessible")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect(frame)

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cls = det["class"]
            label = CLASS_NAMES.get(cls, "Unknown")

            if cls == 3:  # number plate
                plate_img = frame[y1:y2, x1:x2]
                text = extract_text(plate_img)
                color = detect_color(plate_img)
                label = f"{label} | {text} | {color}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(
                frame,
                label,
                (x1, max(30, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow("Agricultural Vehicle Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()
