import cv2
import numpy as np

def detect_color(image):
    if image is None or image.size == 0:
        return "UNKNOWN"

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    avg_hue = hsv[:, :, 1].mean()

    if avg_hue < 50:
        return "White"
    elif avg_hue < 120:
        return "Yellow"
    else:
        return "Other"
