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
turndDirection="init"
skip_obstacles=True


camera = Camera()


def moveForward():
    robot.move(80, 80, 0)

def turnLeft():
    robot.move(0, 80, 0)

def turnRight():
    robot.move(80,0,0)



def initializedetectingObject():
    objectPresent=False
    global turndDirection

    while(not objectPresent):
        objectPresent,isGrabed,pixel_distance,*_=getBoxdata()
        if(not objectPresent):
            if(turndDirection=="init"):
                turnLeft() 
            else:
                turnRight()
        else:
            if(turndDirection=="init"):
                if(pixel_distance>0):
                    turndDirection="Right"
                else:
                    turndDirection="Left"
                return
            
        
def moveToBox():
        #no point of moving towards a white color as well fix that
        global direction
        while(True):
            objectPresent,isGrabed,pixel_distance,obstacle_dist=getBoxdata()
            if(isGrabed):
                robot.move(0,0,0) 
                return

            if(objectPresent):
                if (-100<obstacle_dist<100 and skip_obstacles):
                    robot.move(0,0,0)
                    robot.play_on_sound()
                    time.sleep(1)
                    robot.move(-80,-80,0)
                    time.sleep(1)
                    robot.move(0,0,0)
                    robot.play_on_sound()
                    robot.move(80,80,0)
                else:
                    if(pixel_distance>30):
                        robot.move(50,0,0)
                        direction="Right"
                    elif (pixel_distance<-30):
                        robot.move(0,50,0)
                        direction="Left"
                    else:
                        robot.move(80,80,0)

            
           
def place_Box():
    global isGrabed
    robot.move(80,80,0)
    time.sleep(500)
    robot.move(0,0,0)
    robot.play_on_sound()
    for i in range(4):
        robot.move(-60,-60,0)
        time.sleep(0.5)
        robot.play_recharge_sound()

    isGrabed=False



def gotoPlacemnet(detectedcolor):
    global can_place
    global turndDirection
    global direction

    target_found, target_pixel_distance, can_place=getTargetdata(detectedcolor)
    #need to get the placment position data,color,are of the placment positionand so on using the model
    #target detection code
    while(not target_found):
        #need to get the placment position data,color,are of the placment positionand so on using the model
        turnLeft()
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
    annotated_frame,objectPresent,isGrabed,pixel_distance,obstacle_dist=search_box(frame)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return objectPresent,isGrabed,pixel_distance,obstacle_dist



if __name__ == "__main__":
    
    robot = Kobuki()
    
    robot.play_on_sound()
    robot.move(0,0,0)
    
    while len(colorArray)>0:
        color=colorArray[-1]
        robot.play_clean_start_sound()
        robot.play_clean_start_sound()
        initializedetectingObject()#initially check whther a box is detecte 
        moveToBox()
        gotoPlacemnet(color)
        place_Box()
        colorArray.pop()
        robot.play_clean_start_sound()
        robot.play_clean_stop_sound()
        print("done")

    for i in range(4):
        robot.move(-60,-60,0)
        robot.play_recharge_sound()
        time.sleep(0.5)
    robot.move(0,0,0)

        

camera.stop()
cv2.destroyAllWindows()
