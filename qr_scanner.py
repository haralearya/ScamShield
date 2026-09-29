import cv2
import numpy as np
from PIL import Image

def scan_qr(uploaded_file):
    try:
        image = Image.open(uploaded_file).convert("RGB")
        frame = np.array(image)
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(frame)

        if data:
            clean = data.strip()
            is_url = clean.lower().startswith(("http://", "https://", "www."))
            return {"decoded": True, "data": clean, "is_url": is_url}

        return {"decoded": False, "data": "", "is_url": False}
    except Exception:
        return {"decoded": False, "data": "", "is_url": False}
