import cv2
import numpy as np
from ultralytics import YOLO
from yolov8_model import *
from pygrabber.dshow_graph import FilterGraph

graph = FilterGraph()
devices = graph.get_input_devices()
print("Available cameras:", devices)




# Start video capture
src="video/output.avi"

# cap=cv2.VideoCapture(src)
# count=0
# while True:
#     count+=1
#     ret,frame = cap.read()
#     if not ret:
#         print("exiting")
#         break

    

#     # Resize frame to match model input size
#     print("loop")
#     annotated_frame,*_=search_box(frame)
#     annotated_frame,*_=find_target(annotated_frame,"Red")

#     cv2.imshow("YOLOv8 Detection", annotated_frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cv2.destroyAllWindows()