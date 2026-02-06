import cv2
import numpy as np


def extract_cabin_region(img, vehicle_type):
    """
    Extract only hood / cabin / head region from vehicle image
    """
    h, w, _ = img.shape

    if vehicle_type == "tractor":
        # 🚜 Tractor: hood + steering area
        y1 = int(h * 0.45)
        y2 = int(h * 0.75)
        x1 = int(w * 0.35)
        x2 = int(w * 0.70)

    elif vehicle_type == "truck":
        # 🚚 Truck: front cabin only
        y1 = int(h * 0.20)
        y2 = int(h * 0.50)
        x1 = int(w * 0.25)
        x2 = int(w * 0.65)

    else:
        return None

    roi = img[y1:y2, x1:x2]
    return roi if roi.size > 0 else None


def detect_vehicle_color(img, vehicle_type):
    if img is None or img.size == 0:
        return "UNKNOWN"

    roi = extract_cabin_region(img, vehicle_type)
    if roi is None:
        return "UNKNOWN"

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h_ch, s_ch, v_ch = cv2.split(hsv)

    # Remove shadows + glare
    valid = (v_ch > 70) & (v_ch < 230)
    h_ch = h_ch[valid]
    s_ch = s_ch[valid]
    v_ch = v_ch[valid]

    if h_ch.size < 120:
        return "UNKNOWN"

    # =====================
    # STRONG WHITE
    # =====================
    if np.mean(s_ch) < 35 and np.mean(v_ch) > 170:
        return "White"

    # =====================
    # STRONG BLACK
    # =====================
    if np.mean(v_ch) < 80:
        return "Black"

    # =====================
    # COLOR VOTING
    # =====================
    votes = {"Red": 0, "Green": 0, "Blue": 0, "Yellow": 0}

    for h, s in zip(h_ch, s_ch):
        if s < 45:
            continue

        if h < 10 or h > 165:
            votes["Red"] += 1
        elif 15 <= h < 35:
            votes["Yellow"] += 1
        elif 40 <= h < 80:
            votes["Green"] += 1
        elif 90 <= h < 130:
            votes["Blue"] += 1

    dominant = max(votes, key=votes.get)
    total = sum(votes.values())

    if total == 0 or votes[dominant] / total < 0.40:
        return "UNKNOWN"

    return dominant
