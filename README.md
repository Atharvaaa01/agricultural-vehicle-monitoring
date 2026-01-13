Automatic Agricultural Vehicle Monitoring System Using Computer Vision
🚜 Project Overview
This project implements an end-to-end computer vision system for automatic monitoring of agricultural vehicles. The system can detect different types of vehicles (bullock carts, tractors, trucks), identify whether sugarcane is present, detect number plates, extract text using OCR, and determine the plate color.

Key Features
Vehicle Detection: Detects bullock carts, tractors, and trucks
Sugarcane Detection: Identifies if sugarcane is loaded on vehicles
Number Plate Detection: Locates vehicle number plates
OCR Extraction: Extracts text from number plates using EasyOCR
Color Detection: Determines the dominant color of number plates
Real-time Processing: Supports webcam and IP camera (RTSP) streams
REST API: Flask-based API for image-based detection
Custom YOLO Model: Trained on agricultural vehicle dataset
📋 Table of Contents
Installation
Project Structure
Dataset Preparation
Training the Model
Running the System
API Usage
Configuration
Troubleshooting
🔧 Installation
Prerequisites
Python 3.8 or higher
CUDA-capable GPU (optional, for faster training and inference)
Webcam or IP camera (for real-time detection)
Step 1: Clone the Repository
bash
git clone <repository-url>
cd agricultural-vehicle-monitoring
Step 2: Create Virtual Environment
bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Run Setup Script
bash
python setup.py
This will:

Create necessary directories
Download the base YOLOv8 model
Create default configuration files
📁 Project Structure
agricultural-vehicle-monitoring/
│
├── dataset/                    # Dataset folder
│   ├── images/                # Images
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   ├── labels/                # YOLO format annotations
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── data.yaml             # Dataset configuration
│
├── models/                    # Model files
│   ├── yolov8n.pt            # Base model
│   └── best.pt               # Trained model
│
├── src/                       # Source code
│   ├── train_model.py        # Training script
│   ├── inference.py          # Detection inference
│   ├── camera_detector.py    # Real-time camera detection
│   ├── ocr_processor.py      # OCR functionality
│   ├── plate_color_detector.py # Color detection
│   ├── utils.py              # Utility functions
│   └── api.py                # Flask API
│
├── config/                    # Configuration files
│   └── config.yaml
│
├── outputs/                   # Output files
│   ├── detections/           # Detection results
│   ├── logs/                 # Log files
│   └── api_tests/            # API test results
│
├── static/                    # Static files
│   └── test_images/          # Test images
│
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── run_camera.py             # Run camera detection
├── run_api.py                # Run API server
└── test_api.py               # API testing script
📊 Dataset Preparation
Class Definitions
The model detects 5 classes:

0: bullock_cart - Bullock-drawn carts
1: tractor - Agricultural tractors
2: truck - Trucks/lorries
3: sugarcane - Sugarcane cargo
4: number_plate - Vehicle number plates
Annotation Guidelines
Collect Images: Gather 300-500 images of agricultural vehicles
Install LabelImg (annotation tool):
bash
   pip install labelImg
   labelImg
Annotation Process:
Open LabelImg
Select "Open Dir" → Choose dataset/images/train
Select "Change Save Dir" → Choose dataset/labels/train
Select "YOLO" format
Draw bounding boxes for each object
Save annotations
Annotation Format (YOLO):
   <class_id> <x_center> <y_center> <width> <height>
Example (image001.txt):

   1 0.512 0.423 0.234 0.456
   3 0.512 0.423 0.180 0.220
   4 0.612 0.723 0.080 0.040
Dataset Split:
Training: 70% (210-350 images)
Validation: 20% (60-100 images)
Testing: 10% (30-50 images)
Dataset Configuration
Edit dataset/data.yaml:

yaml
train: ../dataset/images/train
val: ../dataset/images/val
test: ../dataset/images/test

nc: 5

names:
  0: bullock_cart
  1: tractor
  2: truck
  3: sugarcane
  4: number_plate
🎓 Training the Model
Basic Training
bash
python -m src.train_model
Advanced Training Options
Edit the training parameters in src/train_model.py:

python
trainer = VehicleDetectionTrainer(
    model_size='n',        # n, s, m, l, x (larger = more accurate, slower)
    epochs=100,            # Number of training epochs
    batch_size=16,         # Batch size (reduce if GPU memory error)
    img_size=640,          # Image size
)
Training Process
Verify Dataset: The script checks dataset structure
Load Pretrained Model: Downloads YOLOv8 base weights
Training: Trains on your custom dataset
Evaluation: Validates on validation set
Save Model: Best model saved to models/best.pt
Training Output
Training logs: runs/train/agricultural_vehicle_detection/
Best weights: models/best.pt
Metrics: mAP, precision, recall
Expected Training Time
CPU: 30-60 minutes per epoch
GPU (CUDA): 2-5 minutes per epoch
🎥 Running the System
1. Real-time Camera Detection
Using Webcam
bash
python run_camera.py
or

bash
python -m src.camera_detector --source 0
Using IP Camera (RTSP)
bash
python run_camera.py --source "rtsp://username:password@ip:port/stream"
Options
bash
python run_camera.py --help

Options:
  --source      Camera source (0 for webcam, or RTSP URL)
  --model       Path to trained model (default: models/best.pt)
  --conf        Confidence threshold (default: 0.5)
  --save        Save output video
  --output      Output video path
Keyboard Controls
'q': Quit
's': Save screenshot
2. Running the API Server
Start Server
bash
python run_api.py
or

bash
python -m src.api --host 0.0.0.0 --port 5000
API Options
bash
python run_api.py --help

Options:
  --host        Host address (default: 0.0.0.0)
  --port        Port number (default: 5000)
  --debug       Enable debug mode
The API will be available at: http://localhost:5000

🌐 API Usage
Endpoints
1. Root Endpoint
GET /
Returns API information

2. Health Check
GET /health
Returns server health status

3. Detect (JSON)
POST /detect
Content-Type: application/json
Request Body:

json
{
  "image": "base64_encoded_image_string"
}
Response:

json
{
  "status": "success",
  "timestamp": "2024-01-09T10:30:00",
  "results": {
    "vehicle_type": "tractor",
    "vehicle_confidence": 0.92,
    "sugarcane_detected": true,
    "sugarcane_confidence": 0.87,
    "number_plate_present": true,
    "number_plate_confidence": 0.76,
    "number_plate_text": "ABC1234",
    "number_plate_color": "Yellow"
  },
  "detections_count": 3
}
4. Detect (Form Data)
POST /detect
Content-Type: multipart/form-data
Form Data:

image: Image file
5. Detect with Annotated Image
POST /detect_with_image
Content-Type: application/json
Response includes:

Detection results (same as /detect)
annotated_image: Base64 encoded image with bounding boxes
Testing the API
Using Python Script
bash
python test_api.py --image static/test_images/test1.jpg
Using cURL
bash
# JSON request
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{"image": "BASE64_IMAGE_STRING"}'

# Form data request
curl -X POST http://localhost:5000/detect \
  -F "image=@path/to/image.jpg"
Using Python Requests
python
import requests
import base64

# Read and encode image
with open('test_image.jpg', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')

# Send request
response = requests.post(
    'http://localhost:5000/detect',
    json={'image': img_data}
)

# Get results
results = response.json()
print(results)
⚙️ Configuration
config/config.yaml
yaml
model:
  size: 'n'                    # Model size (n, s, m, l, x)
  confidence_threshold: 0.5    # Detection confidence threshold
  path: 'models/best.pt'       # Model path

training:
  epochs: 100                  # Training epochs
  batch_size: 16              # Batch size
  image_size: 640             # Image size

camera:
  default_source: 0           # Default camera (0=webcam)
  fps_display: true           # Show FPS counter
  save_output: false          # Auto-save video

api:
  host: '0.0.0.0'            # API host
  port: 5000                  # API port
  debug: false                # Debug mode
🔍 Troubleshooting
Common Issues
1. Model Not Found
Error: Model not found at models/best.pt

Solution: Train the model first

bash
python -m src.train_model
2. CUDA Out of Memory
Error: RuntimeError: CUDA out of memory

Solution: Reduce batch size in train_model.py

python
batch_size=8  # or even 4
3. Camera Not Opening
Error: Failed to open camera

Solutions:

Check camera index: Try --source 1 or --source 2
For IP camera, verify RTSP URL format
Check camera permissions
4. OCR Not Working
Error: OCR returns "N/A"

Solutions:

Ensure number plate is clearly visible
Check image quality and resolution
Try adjusting confidence threshold
5. API Connection Refused
Error: Connection refused

Solution: Make sure API server is running

bash
python run_api.py
Performance Optimization
For Faster Training:
Use smaller model: model_size='n'
Reduce image size: img_size=416
Use GPU with CUDA
Reduce epochs for testing: epochs=50
For Faster Inference:
Use smaller model
Increase confidence threshold: conf=0.6
Reduce camera resolution
Use GPU acceleration
📈 Evaluation Metrics
Model Performance
After training, check metrics in:

runs/train/agricultural_vehicle_detection/results.png
Key Metrics:

mAP@0.5: Mean Average Precision at IoU 0.5
mAP@0.5:0.95: Mean Average Precision at IoU 0.5 to 0.95
Precision: Correct detections / All detections
Recall: Correct detections / All ground truth
Target Performance:

mAP@0.5: > 0.85
mAP@0.5:0.95: > 0.60
Precision: > 0.80
Recall: > 0.75
🎯 Future Enhancements
 Vehicle speed estimation
 License plate recognition for multiple countries
 Vehicle counting and tracking
 Integration with database for logging
 Mobile app for remote monitoring
 Alert system for unauthorized vehicles
 Multi-camera support
 Cloud deployment
📚 References
YOLOv8: Ultralytics Documentation
EasyOCR: EasyOCR GitHub
Flask: Flask Documentation
OpenCV: OpenCV Documentation
👥 Contributors
[Your Name] - Project Developer
[Supervisor Name] - Project Supervisor
📄 License
This project is developed for educational purposes as part of a final year project.

📞 Contact
For questions or support:

Email: your.email@example.com
GitHub: github.com/yourusername
Last Updated: January 2026


