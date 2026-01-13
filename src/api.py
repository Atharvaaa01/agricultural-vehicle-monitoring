from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np

from src.inference import detect
from src.plate_color_detector import detect_color

app = Flask(__name__)
CORS(app)

# MUST MATCH data.yaml ORDER
CLASS_MAP = {
    0: "tractor",
    1: "truck",
    2: "bullock_cart",
    3: "number_plate",
    4: "sugarcane"
}

@app.route("/detect", methods=["POST"])
def detect_api():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    img_bytes = request.files["image"].read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    detections = detect(img)

    response = {
        "vehicle_detected": False,
        "vehicle_type": None,
        "sugarcane_detected": False,
        "number_plate": False,
        "plate_color": None
    }

    best_vehicle_conf = 0.0

    for d in detections:
        cls = d["class"]
        conf = d["conf"]

        # VEHICLE (highest confidence)
        if cls in [0, 1, 2] and conf > best_vehicle_conf:
            response["vehicle_detected"] = True
            response["vehicle_type"] = CLASS_MAP[cls]
            best_vehicle_conf = conf

        # SUGARCANE
        if cls == 4:
            response["sugarcane_detected"] = True

        # NUMBER PLATE (NO OCR)
        if cls == 3:
            x1, y1, x2, y2 = d["bbox"]
            plate_img = img[y1:y2, x1:x2]
            response["number_plate"] = True
            response["plate_color"] = detect_color(plate_img)

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
