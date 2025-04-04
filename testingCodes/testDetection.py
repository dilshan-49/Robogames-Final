import cv2
import numpy as np
from ultralytics import YOLO
from yolov8_model import *
from cam_feed import Camera

cam=Camera()



while True:

    frame = cam.get_frame()
    if frame is None:
        print("exiting")
        break

    print("loop")
    annotated_frame,*_=search_box(frame)
    annotated_frame,*_=find_target(annotated_frame,"Red")

    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()