import cv2
import numpy as np
import time
from kobukidriver import Kobuki
from cam_feed import Camera

from lastModel import *

placedtodirection=False
latestColor=None
direction = "init"
color="unknown"
turndDirection="init"
skip_obstacles=False


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
        objectPresent,isGrabed,pixel_distance=getBoxdata()
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
            
def initializedetectingObject_any():
    objectPresent=False
    global turndDirection

    while(not objectPresent):
        objectPresent,isGrabed,pixel_distance=getBoxdata_any()
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
        count=0
        while(True):
            count+=1
            objectPresent,isGrabed,pixel_distance=getBoxdata_any()
            print("Looking for object")
            if(isGrabed):
                robot.move(0,0,0) 
                return

            if(objectPresent):
                print("Object Present")
                print("Going to object")
                if(pixel_distance>30):
                    robot.move(50,0,0)
                    direction="Right"
                elif (pixel_distance<-30):
                    robot.move(0,50,0)
                    direction="Left"
                else:
                    robot.move(80,80,0)

            else:
                if (count%2==0):
                    turnLeft()
                else:
                    turnRight()


            
           
def place_Box():
    global isGrabed
    print("Placing box")
    for i in range(20):
        robot.move(30,30,0)
        time.sleep(0.3)
    robot.move(0,0,0)
    robot.play_on_sound()
    for i in range(20):
        robot.move(-60,-60,0)
        time.sleep(0.3)
        robot.play_recharge_sound()
    robot.move(0,0,0)
    for i in range(20):
        turnRight()
        time.sleep(0.1)
    robot.move(0,0,0)
    isGrabed=False



def gotoPlacemnet(detectedcolor):
    global can_place
    global turndDirection
    global direction
    if (detectedcolor=="Blue" or detectedcolor=="Green"):
        target_found, target_pixel_distance, can_place=getTargetdata(detectedcolor)
    else:
        target_found, target_pixel_distance, can_place=getTargetdata_any()
    #need to get the placment position data,color,are of the placment positionand so on using the model
    #target detection code
    while(not target_found):
        print(f"Looking for target {detectedcolor}")
        #need to get the placment position data,color,are of the placment positionand so on using the model
        turnLeft()
        if (detectedcolor=="Blue" or detectedcolor=="Green"):
            target_found, target_pixel_distance, can_place=getTargetdata(detectedcolor)
        else:
            target_found, target_pixel_distance, can_place=getTargetdata_any()


    #need to fix
    while(not can_place):
        #need to get the placment position data,color,are of the placment positionand so on using the model
        print(f"going for target {detectedcolor}")
        if(target_pixel_distance>30):
            robot.move(50,0,0)
            direction="Right"
        elif (target_pixel_distance<-30):
            robot.move(0,50,0)
            direction="Left"
        else:
            if (target_found):
                robot.move(80,80,0)
            else:
                robot.move(25,25,0)
        target_found, target_pixel_distance, can_place=getTargetdata_any()

    can_place=False
    return
    



def getTargetdata(color):
    frame = camera.get_frame()
    annotated_frame,target_found, target_pixel_distance, can_place=find_target(frame,color)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return target_found, target_pixel_distance, can_place

def getTargetdata_any():
    frame = camera.get_frame()
    annotated_frame,target_found, target_pixel_distance, can_place=find_target_any(frame)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return target_found, target_pixel_distance, can_place


def getBoxdata():
    frame = camera.get_frame()
    annotated_frame,objectPresent,isGrabed,pixel_distance=search_box(frame)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return objectPresent,isGrabed,pixel_distance

def getBoxdata_any():
    frame = camera.get_frame()
    annotated_frame,objectPresent,isGrabed,pixel_distance=search_box_any(frame)
    cv2.imshow("a",annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return
    return objectPresent,isGrabed,pixel_distance

def rotate():
    for i in range(20):
        turnRight()
        time.sleep(0.1)

if __name__ == "__main__":
    
    robot = Kobuki()
    
    robot.play_on_sound()
    robot.move(0,0,0)
    color=colorArray[-1]
    initializedetectingObject()
    while len(colorArray)>0:
        color=colorArray[-1]
        robot.play_clean_start_sound()
        robot.play_clean_start_sound()
        if not(color=="Blue"):
            initializedetectingObject_any()#initially check whther a box is detecte 
        print(f"Detected : {color}")
        moveToBox()
        robot.move(0,0,0)
        for i in range(20):
            robot.move(35,35,0)
        print(f"Moved to : {color}")
        gotoPlacemnet(color)
        robot.move(0,0,0)
        print("went to target")
        place_Box()
        prev_color=colorArray.pop()
        robot.play_clean_start_sound()
        robot.play_clean_stop_sound()
        print("done")

    for i in range(25):
        robot.move(-60,-60,0)
        robot.play_recharge_sound()
        time.sleep(0.5)
    robot.move(0,0,0)
    rotate()
    
        

camera.stop()
cv2.destroyAllWindows()
exit()

