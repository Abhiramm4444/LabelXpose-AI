from flask import Flask, render_template, request, redirect
import cv2
import pytesseract
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# List of suspicious ingredients
suspicious_ingredients = [
    "high fructose corn syrup",
    "artificial flavor",
    "monosodium glutamate",
    "sodium nitrate",
    "natural flavor",
    "sodium benzoate",
    "aspartame",
    "preservative",
    "msg"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_label():
    # Capture image from webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error accessing webcam"

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Failed to capture image"

    image_path = os.path.join(UPLOAD_FOLDER, 'capture.jpg')
    cv2.imwrite(image_path, frame)

    # Process image using OCR
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_img).lower()

    # Detect suspicious ingredients
    detected = [item for item in suspicious_ingredients if item in text]

    return render_template('result.html', detected=detected, image_path=image_path, full_text=text)

if __name__ == '__main__':
    app.run(debug=True)
