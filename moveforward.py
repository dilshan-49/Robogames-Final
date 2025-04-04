import cv2
import numpy as np
import time
from kobukidriver import Kobuki

robot = Kobuki()

def moveForward():
    robot.move(80, 80, 0)

def turnLeft():
    robot.move(0, 80, 0)

def turnRight():
    robot.move(80,0,0)

def rotate():
    for i in range(20):
        turnRight()
        time.sleep(0.1)

if __name__ == "__main__":
    
    
    
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
    rotate()
    robot.move(0,0,0)




        
