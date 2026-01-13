import easyocr
import cv2
import numpy as np
import re

reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image):
    if image is None or image.size == 0:
        return "UNKNOWN"

    # 1️⃣ Resize (very important)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 2️⃣ Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3️⃣ Remove noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # 4️⃣ Threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )

    # 5️⃣ OCR
    results = reader.readtext(
        thresh,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        detail=0
    )

    if not results:
        return "UNKNOWN"

    text = max(results, key=len)

    # 6️⃣ Indian number plate regex
    match = re.search(r'[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}', text)
    if match:
        return match.group()

    return text
