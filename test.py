import cv2
import numpy as np
import time
from kobukidriver import Kobuki
import threading

running=True
direction = "Stop"
distanceFromCenter = 50 #this can vary from -360 to +360
color="red"
boxinArms=False

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

def isplacementColordetected(color):
    pass

def searchForPlacementColor(color):
    while True: 
        robot.move(0,80,0)
        time.sleep(2)  # Pause before next recording
        if(isplacementColordetected(color)):
            stop()
            break

def isBoxGrabbed(frame):
    #in the lower part of the frame can see a color the box is taken
    pass

def isObjectDetected():
    pass

def CheckForBox():
    #Run Tharushas model to detect the objects 
    pass

def control_robot(direction,color,distanceFromCenter):
    """Controls the robot based on detected direction."""
    pass
    # while running:
    #     if direction == "Forward":
    #         print("Moving Forward")  # 
    #         robot.move(80, 80, 0)
    #     elif direction == "Left":
    #         print("Turning Left")  # 
    #         robot move(40, 80, 0)
    #     elif direction == "Right":
    #         print("Turning Right")  # 
    #         robot.move(80, 40, 0)
    #     elif direction == "Stop":
    #         print("Stopping")  # 
    #         robot.move(0, 0, 0)
        
    #    time.sleep(0.1)  # Prevents CPU overuse

def isLowerMiddlePartBlack(frame):
    """Check if the lower middle part of the frame is black."""
    height, width, _ = frame.shape
    lower_middle_part = frame[int(0.75 * height):height, int(0.4 * width):int(0.6 * width)]
    black_pixels = np.sum(np.all(lower_middle_part == [0, 0, 0], axis=-1))
    total_pixels = lower_middle_part.shape[0] * lower_middle_part.shape[1]
    return black_pixels < total_pixels * 0.5  # Adjust threshold as needed

if __name__ == "__main__":
    #distance to the nearest object from the middle of the screen
    
    #robot = Kobuki()

    # robot_thread = threading.Thread(target=control_robot)
    # robot_thread.daemon = True
    # robot_thread.start()
    
    #robot.play_on_sound()
    #on the cameras
    #robot.move(0,0,0)#stop initially
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Failed to open camera.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break
        
        # Draw a rectangle in the lower middle part of the frame
        height, width, _ = frame.shape
        print(height,width)
        start_point = (int(0.4 * width), int(0.75 * height))
        end_point = (int(0.6 * width), height)
        color = (0, 255, 0)  # Green color
        thickness = 2
        cv2.rectangle(frame, start_point, end_point, color, thickness)
        
        if isLowerMiddlePartBlack(frame):
            print("Lower middle part is not black")
        else:
            print("Lower middle part is black")
        
        #boxinArms = isBoxGrabbed(frame)
        #if boxinArms:
            print("Box is taken")
            #searchForPlacementColor()
        #if isObjectDetected():
        #    pass
        
        # Display the frame with the rectangle
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()