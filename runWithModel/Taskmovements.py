import cv2
import numpy as np
import time
from kobukidriver import Kobuki
import yolov8_model 
#import threading

#
direction = "Stop"
pixel_distance = 50 #this can vary from -360 to +360
color="red"

#boxinArms=False
objectPresent=False
isGrabed=False



def moveForward():
    robot.move(80, 80, 0)

def turnLeft():
    robot.move(0, 80, 0)

def stop():
    robot.move(0, 0, 0)

def turnRound():
    while True:
        moveForward()
        time.sleep(4)  # Move for 1 second
        turnLeft()
        time.sleep(4)  # Pause before next recording
        # if(isrecover):
        #     robot_thread.join(timeout=1.0)  
        #     stop()
        #     break
def isplacementColordetected():
    #need to run seperate model to identify the placement color
    #need to ditect the color in the middle of the frame
    pass
def searchForPlacementColor(color):
        while True: 
            robot.move(0,80,0)
            time.sleep(2)  # Pause before next recording
            if(isplacementColordetected(color)):
                stop()
                return True
            
            
def movetothedestination():
    pass
def turntoDetectObject():
    pass
def control_robot(direction,color,pixel_distance):
    """Controls the robot based on detected direction."""

    pass

if __name__ == "__main__":
    #distance to the nearest object from the middle of the screen
    
    robot = Kobuki()

    # robot_thread = threading.Thread(target=control_robot)
    # robot_thread.daemon = True
    # robot_thread.start()
    
    robot.play_on_sound()
    #on the cameras
    robot.move(0,0,0)#stop initially
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Failed to open camera.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        annotated_frame,objectPresent,isGrabed,pixel_distance,color=predict_frame(frame)
        
        if(objectPresent):
            if(pixel_distance>20):
                robot.move(80,0,0)
                direction="Right"
            elif (pixel_distance<-20):
                robot.move(0,80,0)
                direction="Left"
            else:
                robot.move(80,80,0)
                direction="Forward"

        if(isGrabed):
            print("Box is taken")
            robot.play_error_sound()
            # placedtodirection=searchForPlacementColor()
            # if(placedtodirection):
            #     movetothedestination()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
        






    
