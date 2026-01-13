import cv2
from src.ocr_processor import extract_text
from src.plate_color_detector import detect_color

img = cv2.imread("dataset/images/train/truck.jpg")

text = extract_text(img)
color = detect_color(img)

print("Number Plate Text:", text)
print("Plate Color:", color)
