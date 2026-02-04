import os
os.environ["ULTRALYTICS_DISABLE_CV2_IMSHOW"] = "1"

import cv2
import time
from src.inference import detect
from src.ocr_processor import extract_text
from src.plate_color_detector import detect_color


# CLASS INDEX → LABEL (must match training)
CLASS_NAMES = {
    0: "Tractor",
    1: "Truck",
    2: "Bullock Cart",
    3: "Number Plate",
    4: "Sugarcane"
}


def run_camera(source):
    """
    source:
        0               -> webcam
        rtsp://...      -> IP camera
    """

    print(f"[INFO] Opening video source: {source}")

    cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)

    # 🔴 RTSP stability settings
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, 15)

    if not cap.isOpened():
        raise RuntimeError("❌ Unable to open video source")

    last_frame_time = time.time()

    while True:
        ret, frame = cap.read()

        # 🔁 Reconnect if stream breaks
        if not ret or frame is None:
            print("⚠️ Frame not received. Reconnecting...")
            cap.release()
            time.sleep(2)
            cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            continue

        # 🔹 Resize for better FPS (IMPORTANT)
        frame = cv2.resize(frame, (960, 540))

        detections = detect(frame)

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cls = det["class"]
            conf = det.get("conf", 0.0)

            label = CLASS_NAMES.get(cls, "Unknown")
            label = f"{label} {conf:.2f}"

            # 🟡 Number plate processing
            if cls == 3:
                plate_img = frame[y1:y2, x1:x2]

                if plate_img.size > 0:
                    text = extract_text(plate_img)
                    color = detect_color(plate_img)
                    label = f"{label} | {text} | {color}"

            # 🟢 Bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 🏷 Label
            cv2.putText(
                frame,
                label,
                (x1, max(30, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow("Agricultural Vehicle Monitoring (RTSP)", frame)

        # ESC to exit
        if cv2.waitKey(1) & 0xFF == 27:
            print("[INFO] Exit requested")
            break

    cap.release()
    cv2.destroyAllWindows()
