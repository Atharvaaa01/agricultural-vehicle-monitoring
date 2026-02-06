from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

from src.inference import detect
from src.plate_color_detector import detect_color
from src.ocr_processor import extract_text
from src.vehicle_color_detector import detect_vehicle_color

app = Flask(__name__)
CORS(app)

CLASS_MAP = {
    0: "tractor",
    1: "truck",
    2: "bullock_cart",
    3: "number_plate",
    4: "sugarcane"
}


# -----------------------------
# Helpers
# -----------------------------
def plate_inside_vehicle(plate_bbox, vehicle_bbox):
    px1, py1, px2, py2 = plate_bbox
    vx1, vy1, vx2, vy2 = vehicle_bbox
    cx = (px1 + px2) // 2
    cy = (py1 + py2) // 2
    return vx1 <= cx <= vx2 and vy1 <= cy <= vy2


def vehicle_score(v):
    score = v["conf"]
    if v["class"] == 1:   # boost truck
        score += 0.15
    return score


# -----------------------------
# API
# -----------------------------
@app.route("/detect", methods=["POST"])
def detect_api():
    if "image" not in request.files:
        return jsonify({"error": "No image"}), 400

    img_bytes = request.files["image"].read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    detections = detect(img)

    vehicles, plates = [], []
    sugarcane_boxes = []

    for d in detections:
        if d["class"] in [0, 1, 2]:
            vehicles.append(d)
        elif d["class"] == 3:
            plates.append(d)
        elif d["class"] == 4:
            sugarcane_boxes.append(d["bbox"])

    response = {
        "vehicle_detected": False,
        "vehicle_type": None,
        "vehicle_color": None,
        "load_status": "UNKNOWN",
        "number_plate": None,
        "plate_color": None
    }

    # -----------------------------
    # VEHICLE FOUND
    # -----------------------------
    if vehicles:
        vehicle = max(vehicles, key=vehicle_score)
        vx1, vy1, vx2, vy2 = vehicle["bbox"]

        w = vx2 - vx1
        h = vy2 - vy1
        aspect_ratio = w / h

        vehicle_type = CLASS_MAP[vehicle["class"]]
        if vehicle_type == "tractor" and aspect_ratio > 1.6:
            vehicle_type = "truck"

        response["vehicle_detected"] = True
        response["vehicle_type"] = vehicle_type

        vehicle_img = img[vy1:vy2, vx1:vx2]
        response["vehicle_color"] = detect_vehicle_color(vehicle_img, vehicle_type)

        # -----------------------------
        # LOAD STATUS (IoU BASED)
        # -----------------------------
        response["load_status"] = "EMPTY"
        for sx1, sy1, sx2, sy2 in sugarcane_boxes:
            cx = (sx1 + sx2) // 2
            cy = (sy1 + sy2) // 2
            if vx1 <= cx <= vx2 and vy1 <= cy <= vy2:
                response["load_status"] = "SUGARCANE"
                break

        # -----------------------------
        # NUMBER PLATE
        # -----------------------------
        for p in plates:
            if plate_inside_vehicle(p["bbox"], vehicle["bbox"]):
                px1, py1, px2, py2 = p["bbox"]
                plate_img = img[py1:py2, px1:px2]

                text = extract_text(plate_img)
                if text != "UNKNOWN":
                    response["number_plate"] = text
                    response["plate_color"] = detect_color(plate_img)
                break

    # -----------------------------
    # PLATE ONLY IMAGE
    # -----------------------------
    else:
        plate_text = extract_text(img)
        if plate_text != "UNKNOWN":
            response["number_plate"] = plate_text
            response["plate_color"] = detect_color(img)

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
