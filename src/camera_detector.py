import os
os.environ["ULTRALYTICS_DISABLE_CV2_IMSHOW"] = "1"

import cv2
import time

from src.inference import detect
from src.ocr_processor import extract_text
from src.plate_color_detector import detect_color
from src.vehicle_color_detector import detect_vehicle_color


CLASS_NAMES = {
    0: "TRACTOR",
    1: "TRUCK",
    2: "BULLOCK CART",
    3: "NUMBER PLATE",
    4: "SUGARCANE"
}


def plate_inside_vehicle(plate_bbox, vehicle_bbox):
    px1, py1, px2, py2 = plate_bbox
    vx1, vy1, vx2, vy2 = vehicle_bbox
    cx = (px1 + px2) // 2
    cy = (py1 + py2) // 2
    return vx1 <= cx <= vx2 and vy1 <= cy <= vy2


def vehicle_score(v):
    score = v["conf"]
    if v["class"] == 1:  # boost truck
        score += 0.15
    return score


def run_camera(source=0):
    print("[INFO] Starting camera...")

    cap = cv2.VideoCapture(source)
    time.sleep(2)

    if not cap.isOpened():
        raise RuntimeError("❌ Camera not opened")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame not received")
            break

        frame = cv2.resize(frame, (960, 540))
        detections = detect(frame)

        vehicles = []
        plates = []

        for d in detections:
            if d["class"] in [0, 1, 2]:
                vehicles.append(d)
            elif d["class"] == 3:
                plates.append(d)

        if vehicles:
            vehicle = max(vehicles, key=vehicle_score)
            vx1, vy1, vx2, vy2 = vehicle["bbox"]

            vehicle_type = CLASS_NAMES.get(vehicle["class"], "UNKNOWN")

            # 🔹 Vehicle color
            vehicle_img = frame[vy1:vy2, vx1:vx2]
            vehicle_color = detect_vehicle_color(vehicle_img, vehicle_type.lower())

            # 🔹 Plate detection
            plate_text = "NOT FOUND"
            plate_color = ""

            for p in plates:
                if plate_inside_vehicle(p["bbox"], vehicle["bbox"]):
                    px1, py1, px2, py2 = p["bbox"]
                    plate_img = frame[py1:py2, px1:px2]
                    if plate_img.size > 0:
                        plate_text = extract_text(plate_img)
                        plate_color = detect_color(plate_img)
                    break

            # 🔹 LABEL (exactly like your screenshot)
            label = f"{vehicle_type} | {vehicle_color}"
            if plate_text != "UNKNOWN":
                label += f" | {plate_text}"
            if plate_color:
                label += f" | {plate_color}"

            # 🔹 DRAW BOX
            cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (0, 255, 0), 2)

            # 🔹 DRAW TEXT
            cv2.putText(
                frame,
                label,
                (vx1, max(30, vy1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow("Agricultural Vehicle Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
