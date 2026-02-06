import os
os.environ["ULTRALYTICS_DISABLE_CV2_IMSHOW"] = "1"

import cv2
import time
from src.inference import detect
from src.ocr_processor import extract_text
from src.plate_color_detector import detect_color
from src.vehicle_color_detector import detect_vehicle_color


# ==========================
# MODEL CLASS MAP
# ==========================
CLASS_NAMES = {
    0: "tractor",
    1: "truck",
    2: "bullock_cart",
    3: "number_plate",
}


def inside(b1, b2):
    """Check if center of b1 is inside b2"""
    x1, y1, x2, y2 = b1
    X1, Y1, X2, Y2 = b2
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return X1 <= cx <= X2 and Y1 <= cy <= Y2


def vehicle_score(v):
    """Boost truck confidence slightly"""
    score = v["conf"]
    if v["class"] == 1:  # truck
        score += 0.15
    return score


def run_camera(source):
    print(f"[INFO] Opening RTSP stream: {source}")

    cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        raise RuntimeError("❌ Unable to open RTSP stream")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Stream lost, reconnecting...")
            time.sleep(1)
            cap.release()
            cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            continue

        frame = cv2.resize(frame, (960, 540))
        detections = detect(frame)

        vehicles, plates = [], []

        for d in detections:
            if d["class"] in [0, 1, 2]:
                vehicles.append(d)
            elif d["class"] == 3:
                plates.append(d)

        if vehicles:
            v = max(vehicles, key=vehicle_score)
            vx1, vy1, vx2, vy2 = v["bbox"]

            # ==========================
            # VEHICLE TYPE FIX
            # ==========================
            w = vx2 - vx1
            h = vy2 - vy1
            aspect = w / max(h, 1)

            vtype = CLASS_NAMES[v["class"]]
            if vtype == "tractor" and aspect > 1.6:
                vtype = "truck"

            # ==========================
            # VEHICLE COLOR
            # ==========================
            vehicle_img = frame[vy1:vy2, vx1:vx2]
            vcolor = detect_vehicle_color(vehicle_img, vtype)

            # ==========================
            # NUMBER PLATE
            # ==========================
            plate_text = "NO PLATE"
            plate_color = ""

            for p in plates:
                if inside(p["bbox"], v["bbox"]):
                    px1, py1, px2, py2 = p["bbox"]
                    plate_img = frame[py1:py2, px1:px2]
                    if plate_img.size > 0:
                        plate_text = extract_text(plate_img)
                        plate_color = detect_color(plate_img)
                    break

            # ==========================
            # FINAL LABEL
            # ==========================
            label = f"{vtype.upper()} | {vcolor} | {plate_text}"
            if plate_color:
                label += f" | {plate_color}"

            cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                label,
                (vx1, max(30, vy1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow("Agricultural Vehicle Monitoring (RTSP)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
