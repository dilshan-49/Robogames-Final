import cv2
import numpy as np
from ultralytics import YOLO
from kobukidriver import Kobuki

# Load YOLOv8 model
model = YOLO("weights/best_float32.tflite")

# Start video capture
cap = cv2.VideoCapture("robogames.avi")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

  
    # Run inference
    results = model(frame,conf = 0.7)

    # Process & display output
    annotated_frame = results[0].plot()


    frame_hieght, frame_width, _ = frame.shape
    mid_vertical_line = frame_width//2

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x_center = (x1 + x2) // 2
            y_center = (y1 + y2) // 2

            pixel_distance = abs(mid_vertical_line - x_center)

            cv2.circle(annotated_frame, (int(x_center), int(y_center)), 5, (0, 255, 0), -1)
            cv2.putText(annotated_frame, f"Dist: {pixel_distance:.2f}px", (int(x_center), int(y_center) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


def main():
    pass

if __name__ == "__main__":
    model = YOLO("weights/best_float32.tflite")
    robot=Kobuki()


cap.release()
cv2.destroyAllWindows()