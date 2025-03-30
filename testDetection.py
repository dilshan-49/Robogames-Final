import cv2
import numpy as np
from ultralytics import YOLO
from yolov8_model import *
from cam_feed import Camera

cam=Camera()

# Start video capture

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()


while True:
    count+=1
    frame = cam.get_frame()
    if frame is None:
        print("exiting")
        break

    # ret,frame = cap.read()
    # if not ret:
    #     print("Error: Unable to read from the camera.")
    #     break

    # Resize frame to match model input size
    print("loop")
    annotated_frame,*_=search_box(frame)
    annotated_frame,*_=find_target(annotated_frame,"Red")

    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()