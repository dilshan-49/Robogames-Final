import cv2
import numpy as np
import time
from kobukidriver import Kobuki
from cam_feed import Camera

from yolov8_model import *

placedtodirection=False
latestColor=None
direction = "Stop"
color="Unknown"
camera = Camera()

def moveForward():
    robot.move(80, 80, 0)

def turnLeft():
    robot.move(0, 80, 0)



def turnRound():
    while True:
        moveForward()
        time.sleep(4)  # Move for 1 second
        turnLeft()
        time.sleep(4)  
        # if(isrecover):
        #     robot_thread.join(timeout=1.0)  
        #     robot.move(0,0,0)
        #     break


#--------------------------------------------------------------------------------------------
def avoidWhite():
    if(color=="White"):
        if(pixel_distance>30):
            robot.move(0,50,0)
            direction="Left"
        elif (pixel_distance<-30):
            robot.move(50,0,0)
            direction="Right"
        else:
            #have to change the code here to move when the obstruct meet in the front
            #check about the area to make a decision
            robot.move(-80,-80,0)
            direction="Forward"

def isplacementColordetected(searchcolor):
    #need to run seperate model to identify the placement color
    #need to ditect the color in the middle of the frame
    #####################################################################################
    annotated_frame,objectPresent,isGrabed,pixel_distance,color=predict_frame(frame)#here we have to return the colors of placement positons by the model
    #####################################################################################

    #here now we can change the functionalos of the model to detect the color of the placement position
    if(color==searchcolor):
        return True
    else:
        return False

def searchForPlacementColor(color):
        while True: 
            robot.move(0,80,0)#need to define what would be the movement
            time.sleep(2)  #find a good method
            if(isplacementColordetected(color)):
                robot.move(0,0,0)
                return True
            
            
def movetothedestination():
    #content goes here
    #if it meets the white obstruct has to avoid it
    placedtodirection=False
    pass
def turntoDetectObject():
    if(direction=="left"):
        robot.move(0,80,0)
    pass

<<<<<<< HEAD
=======
    pass

>>>>>>> a6ade64076e8d7cf78a6f0ea02868863ba3a71fe
if __name__ == "__main__":
    
    robot = Kobuki()
    
    robot.play_on_sound()
    robot.move(0,0,0)

    while True:

        frame = camera.get_frame()

        annotated_frame,objectPresent,isGrabed,pixel_distance,color=predict_frame(frame)
<<<<<<< HEAD

        if(color is not None):
            print("Color detected is : ",color)
            latestColor=color#conflict here
                            #color changes rapidly if that detect somme another object with little higher area

        if(objectPresent):#Here need to avoid detecting the placed colors as well
            if(pixel_distance>30):
                robot.move(50,0,0)
=======
        
        if(objectPresent):
            if(pixel_distance>20):
                robot.move(80,0,0)
>>>>>>> a6ade64076e8d7cf78a6f0ea02868863ba3a71fe
                direction="Right"
            elif (pixel_distance<-30):
                robot.move(0,50,0)
                direction="Left"
            else:
                robot.move(80,80,0)
                direction="Forward"

        if(isGrabed):
            print("Box is taken")
            robot.play_error_sound()
<<<<<<< HEAD
            placedtodirection=searchForPlacementColor(latestColor)
            if(placedtodirection):
                movetothedestination()
                robot.move(-80,-80,-80)#is one time call is enough
                turnRound()
                

        if((not isGrabed) and (not objectPresent)):
            print("No any object detected")
            turntoDetectObject()
        #if ether box is not detected or box is not grabbed
        #search for the box
        #turntoDetectObject()#wonce a box id detected just let go the loop
        #if detected move towards the object
        #if it doesnt ditect the correct object
        #move to the white obstruct
        cv2.imshow("a",annotated_frame)
=======
            # placedtodirection=searchForPlacementColor()
            # if(placedtodirection):
            #     movetothedestination()
>>>>>>> a6ade64076e8d7cf78a6f0ea02868863ba3a71fe
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
camera.stop()
cv2.destroyAllWindows()
        






    