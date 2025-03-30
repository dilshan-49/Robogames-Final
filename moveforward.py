import cv2
import numpy as np
import time
from kobukidriver import Kobuki

if __name__ == "__main__":
    
    robot = Kobuki()
    
    robot.play_on_sound()
    print("Placing box")
    for i in range(15):
        robot.move(30,30,0)
        time.sleep(0.3)
    robot.move(0,0,0)
    robot.play_on_sound()
    for i in range(20):
        robot.move(-50,-50,0)
        time.sleep(0.3)
        robot.play_recharge_sound()
    robot.move(0,0,0)
    isGrabed=False


        
