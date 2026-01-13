import cv2
from src.ocr_processor import extract_text
from src.plate_color_detector import detect_color

img = cv2.imread("dataset/test/images/00000002_jpg.rf.acd8487b67c4b8136f907732062cccb8.jpg")
#C:\Users\ASUS\Desktop\agricultural-vehicle-monitoring\dataset\test\images\00000002_jpg.rf.acd8487b67c4b8136f907732062cccb8.jpg
text = extract_text(img)
color = detect_color(img)

print("Number Plate Text:", text)
print("Plate Color:", color)
