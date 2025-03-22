import cv2
import numpy as np
import time

def use_camera():
    cam = cv2.VideoCapture(0)
    cv2.waitKey(0) 
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return None, None, None
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Could not read frame.")
            continue

        print(frame.shape)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        cv2.imshow("Camera Frame", img_rgb)
         # Wait indefinitely until a key is pressed
        time.sleep(1)



if __name__ == "__main__":
    while True:
        use_camera()