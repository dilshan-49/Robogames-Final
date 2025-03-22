import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("best_float32.tflite")

# Start video capture
cap = cv2.VideoCapture("robogames.avi")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to match model input size

    results = model(frame)

    # Process & display output
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()