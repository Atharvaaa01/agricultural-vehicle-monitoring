import easyocr
import cv2
import re

# Initialize OCR reader once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image):
    if image is None or image.size == 0:
        return "UNKNOWN"

    # 1️⃣ Resize (helps OCR a lot)
    image = cv2.resize(
        image, None,
        fx=2.5, fy=2.5,
        interpolation=cv2.INTER_CUBIC
    )

    # 2️⃣ Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3️⃣ Morphology to separate overlapping characters (IMPORTANT)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

    # 4️⃣ Noise removal
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # 5️⃣ OCR
    results = reader.readtext(
        gray,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        detail=0
    )

    if not results:
        return "UNKNOWN"

    # 6️⃣ Combine all OCR text (handles 1-line & 2-line plates)
    text = "".join(results)
    text = re.sub(r'[^A-Z0-9]', '', text)

    # 7️⃣ Context-aware correction using Indian plate structure
    # Format: LL DD LL DDDD
    if len(text) >= 8:
        chars = list(text)

        # State code (letters only)
        for i in [0, 1]:
            if chars[i] in ['0', '1', '2', '5', '8']:
                chars[i] = {
                    '0': 'O',
                    '1': 'I',
                    '2': 'Z',
                    '5': 'S',
                    '8': 'B'
                }.get(chars[i], chars[i])

        # District code (digits only) → FIX YOUR OVERLAP ISSUE HERE
        for i in [2, 3]:
            if i < len(chars):
                if chars[i] in ['I', 'L']:
                    chars[i] = '1'
                elif chars[i] == 'H':     # H misread instead of 4
                    chars[i] = '4'
                elif chars[i] == 'O':
                    chars[i] = '0'

        # Series code (letters only)
        for i in [4, 5]:
            if i < len(chars):
                if chars[i] in ['0', '1', '2', '5', '8']:
                    chars[i] = {
                        '0': 'O',
                        '1': 'I',
                        '2': 'Z',
                        '5': 'S',
                        '8': 'B'
                    }.get(chars[i], chars[i])

        # Last 4 digits
        for i in range(len(chars) - 4, len(chars)):
            if i >= 0:
                if chars[i] in ['O', 'Q', 'D']:
                    chars[i] = '0'
                elif chars[i] in ['I', 'L']:
                    chars[i] = '1'
                elif chars[i] == 'S':
                    chars[i] = '5'
                elif chars[i] == 'B':
                    chars[i] = '8'

        text = "".join(chars)

    # 8️⃣ Final Indian number plate validation
    pattern = r'[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}'
    match = re.search(pattern, text)

    if match:
        return match.group()

    return text if len(text) >= 6 else "UNKNOWN"
