# 🚜 Agricultural Vehicle Monitoring System (Vision AI)

An end-to-end **Computer Vision–based Agricultural Monitoring System** that detects agricultural vehicles, sugarcane loads, and number plates using **YOLOv8**, **Flask API**, and a **lightweight web frontend**.

This project is designed for **smart agriculture, traffic monitoring, and compliance checking** use cases.

---

## 📌 Features

✅ Detects **Agricultural Vehicles**
- Tractor  
- Truck  
- Bullock Cart  

✅ Detects **Sugarcane Presence**

✅ Detects **Number Plate Region**
- Plate color detection
- OCR intentionally disabled for reliability

✅ Supports:
- Image upload via web UI
- Real-time camera detection
- REST API integration

---

## 🧠 Tech Stack

### 🔹 Machine Learning
- YOLOv8 (Ultralytics)
- PyTorch
- OpenCV

### 🔹 Backend
- Flask
- Flask-CORS
- REST API

### 🔹 Frontend
- HTML
- CSS (Glassmorphism UI)
- Vanilla JavaScript (Fetch API)

## 📂 Project Structure
agricultural-vehicle-monitoring/
│
├── dataset/
│ ├── train/
│ ├── valid/
│ ├── test/
│ └── data.yaml
│
├── runs/
│
├── src/
│ ├── api.py
│ ├── inference.py
│ ├── camera_detector.py
│ ├── ocr_processor.py
│ ├── plate_color_detector.py
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── run_api.py
├── run_camera.py
├── requirements.txt
├── README.md
└── yolov8n.pt


---

## 📊 Model Classes

| Class ID | Class Name |
|--------:|-----------|
| 0 | Tractor |
| 1 | Truck |
| 2 | Bullock Cart |
| 3 | Number Plate |
| 4 | Sugarcane |

---

