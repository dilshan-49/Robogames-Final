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
    # while running:
    #     if direction == "Forward":
    #         print("Moving Forward")  # 
    #         robot.move(80, 80, 0)
    #     elif direction == "Left":
    #         print("Turning Left")  # 
    #         robot.move(40, 80, 0)
    #     elif direction == "Right":
    #         print("Turning Right")  # 
    #         robot.move(80, 40, 0)
    #     elif direction == "Stop":
    #         print("Stopping")  # 
    #         robot.move(0, 0, 0)
        
    #    time.sleep(0.1)  # Prevents CPU overuse
def predict_frame(frame,model):
    pass

    # Predict the direction
    #direction = model.predict(frame)
    #direction = np.argmax(direction)
    #direction = classes[direction]

    # Predict the distance
    #distance = model.predict(frame)
    #distance = np.argmax(distance)
    #distance = classes[distance]
    #print("Direction: ", direction)
    #print("Distance: ", distance)
    #return direction, distance
    return 50,"red",True,False
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
        
        #import the model
        #run the model
        #depnd on the object get several detaied information
        #get the direction of the object
        #pixel_distance,color,area,objectpresent,isboxgrabbed=getdeteilsfromthemodel()
        #have to controll the robot according to the position
        
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
        #if ether box is noot detected or box is not grabbed
        #search for the box
        #turntoDetectObject()#wonce a box id detected just let go the loop
        #if detected move towards the object
        #if it doesnt ditect the correct object
        #move to the white obstruct
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
        






    
