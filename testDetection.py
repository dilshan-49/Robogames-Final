import cv2
import numpy as np
from ultralytics import YOLO
from yolov8_model import *
from threading import Thread


class Camera:
    def __init__(self,source=0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise Exception("Error: Unable to access the camera.")
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def get_frame(self):
        if self.ret:
            return self.frame
        return None
    
    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()



# Start video capture
src="video/RobboGmaes_4.avi"

cap=cv2.VideoCapture(src)
count=0
while True:
    count+=1
    ret,frame = cap.read()
    if not ret:
        print("exiting")
        break
    if count%10!=0:
        continue
    

    # Resize frame to match model input size
    print("loop")
    annotated_frame,*_=search_box(frame)
    annotated_frame,*_=find_target(annotated_frame,"Red")

    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()