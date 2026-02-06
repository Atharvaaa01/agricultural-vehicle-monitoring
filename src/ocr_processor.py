import easyocr
import cv2
import re

# Initialize OCR reader once
reader = easyocr.Reader(['en'], gpu=False)

# Strict Indian plate format: AA00AA0000
PLATE_PATTERN = re.compile(r'[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}')

def extract_text(image):
    if image is None or image.size == 0:
        return "UNKNOWN"

    # 1️⃣ Resize (very important for OCR)
    image = cv2.resize(
        image, None,
        fx=2.5, fy=2.5,
        interpolation=cv2.INTER_CUBIC
    )

    # 2️⃣ Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3️⃣ Adaptive threshold (better than OPEN for plates)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 15
    )

    # 4️⃣ Morphology to close gaps between characters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    # 5️⃣ OCR
    results = reader.readtext(
        gray,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        detail=0
    )

    if not results:
        return "UNKNOWN"

    # 6️⃣ Combine all OCR text
    raw_text = "".join(results)
    raw_text = re.sub(r'[^A-Z0-9]', '', raw_text)

    # 7️⃣ CHARACTER CORRECTION (Indian plates)
    corrected = []

    for ch in raw_text:
        corrected.append({
            'O': '0',
            'Q': '0',
            'D': '0',
            'I': '1',
            'L': '1',
            'Z': '2',
            'S': '5',
            'B': '8'
        }.get(ch, ch))

    corrected_text = "".join(corrected)

    # 8️⃣ STRICT PLATE MATCH ONLY
    match = PLATE_PATTERN.search(corrected_text)

    if match:
        return match.group()

    # ❌ Do not return noisy / partial text
    return "UNKNOWN"
