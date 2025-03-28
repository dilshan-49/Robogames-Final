import cv2
import numpy as np
import time
from kobukidriver import Kobuki
from cam_feed import Camera
from collections import Counter

from yolov8_model import *

placedtodirection=False
latestColor=None
direction = "init"
color="unknown"
colorArray=["Red","Green","Blue","Yellow"]
turndDirection="Left"
camera = Camera()


def moveForward():
    robot.move(80, 80, 0)

def turnLeft():
    robot.move(0, 80, 0)

def turnRight():
    robot.move(80,0,0)

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
# def avoidWhite():
#     if(color=="White"):
#         if(pixel_distance>30):
#             robot.move(0,50,0)
#             direction="Left"
#         elif (pixel_distance<-30):
#             robot.move(50,0,0)
#             direction="Right"
#         else:
#             #have to change the code here to move when the obstruct meet in the front
#             #check about the area to make a decision
#             robot.move(-80,-80,0)
#             direction="Forward"

# def isplacementColordetected(searchcolor):
#     #need to run seperate model to identify the placement color
#     #need to ditect the color in the middle of the frame
#     #####################################################################################
#     annotated_frame,objectPresent,isGrabed,pixel_distance,color=predict_frame(frame)#here we have to return the colors of placement positons by the model
#     #####################################################################################

#     #here now we can change the functionalos of the model to detect the color of the placement position
#     if(color==searchcolor):
#         return True
#     else:
#         return False

# def searchForPlacementColor(color):
#         while True: 
#             robot.move(0,80,0)#need to define what would be the movement
#             time.sleep(2)  #find a good method
#             if(isplacementColordetected(color)):
#                 robot.move(0,0,0)
#                 return True
            
            
# def movetothedestination():
#     #content goes here
#     #if it meets the white obstruct has to avoid it
#     placedtodirection=False
#     pass
# def turntoDetectObject():
#     if(direction=="left"):
#         robot.move(0,80,0)
#     pass
#----------------------------------------------
def initializedetectingObject():
    objectPresent=False
    global turndDirection

    while(not objectPresent):
        objectPresent,isGrabed,pixel_distance,color=getBoxdata()
        if(not objectPresent):
            if(direction=="init"):
                turnLeft() 
            elif(turndDirection=="Right"):
                turnLeft()
            elif(turndDirection=="Left"):
                turnRight()
        else:
            if(direction=="init"):
                if(pixel_distance>0):
                    turndDirection="Right"
                else:
                    turndDirection="Left"
                return
            
        
def moveToBox():
        #no point of moving towards a white color as well fix that
        detectedcolor=[]
        count=0
        while(True):
            objectPresent,isGrabed,pixel_distance,color=getBoxdata()
            if(isGrabed):
                robot.move(0,0,0) 
                return color

            if(objectPresent):
                if(color in colorArray and count<5):
                    detectedcolor.append(color)
                    count+=1
                
                if(pixel_distance>30):
                    robot.move(50,0,0)
                    direction="Right"
                elif (pixel_distance<-30):
                    robot.move(0,50,0)
                    direction="Left"
                else:
                    robot.move(80,80,0)
        robot.move(0,0,0) 
           
def place_Box():
    global isGrabed
    robot.move(60,60,0)
    time.sleep(1)
    robot.move(0,0,0)
    robot.play_on_sound()
    robot.move(-80,-80,0)
    time.sleep(1)
    robot.move(-80,-80,0)
    isGrabed=False



def gotoPlacemnet(detectedcolor):
    global can_place
    global turndDirection

    target_found, target_pixel_distance, can_place=getTargetdata(detectedcolor)
    #need to get the placment position data,color,are of the placment positionand so on using the model
    #target detection code
    while(not target_found):
        #need to get the placment position data,color,are of the placment positionand so on using the model
        if(turndDirection=="Left"):
            turnLeft()
            turndDirection="Left"
        if(turndDirection=="Right"):
            turnRight()
            turndDirection="Right"

        target_found, target_pixel_distance, can_place=getTargetdata(detectedcolor)


    #need to fix
    while(not can_place):
        #need to get the placment position data,color,are of the placment positionand so on using the model
        if(target_pixel_distance>30):
            robot.move(50,0,0)
            direction="Right"
        elif (target_pixel_distance<-30):
            robot.move(0,50,0)
            direction="Left"
        else:
            robot.move(80,80,0)
        target_found, target_pixel_distance, can_place=getTargetdata(detectedcolor)

    place_Box()
    colorArray.remove(detectedcolor)


    return
    



def getTargetdata(color):
    frame = camera.get_frame()
    annotated_frame,target_found, target_pixel_distance, can_place=find_target(frame,color)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return target_found, target_pixel_distance, can_place

def getBoxdata():
    frame = camera.get_frame()
    annotated_frame,objectPresent,isGrabed,pixel_distance,color=search_box(frame)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return objectPresent,isGrabed,pixel_distance,color

if __name__ == "__main__":
    
    robot = Kobuki()
    
    robot.play_on_sound()
    robot.move(0,0,0)
    
    initializedetectingObject()#initially check whther a box is detecte 
    detectedcolor=moveToBox()
    gotoPlacemnet(detectedcolor)
    robot.move(-60,80,0)
    time.sleep(1)
    robot.move(0,0,0)
    robot.play_on_sound()
    robot.play_on_sound()
    robot.play_on_sound()
    print("done")

    

        

camera.stop()
cv2.destroyAllWindows()
        






    