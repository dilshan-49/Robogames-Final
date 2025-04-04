import cv2
import numpy as np
import time
from kobukidriver import Kobuki

if __name__ == "__main__":
    
    robot = Kobuki()
    
    robot.play_on_sound()

    robot.move(0,0,0)
    
    for i in range(10):
        robot.move(80,80,0)
        time.sleep(0.3)
    robot.move(0,0,0)

    robot.play_on_sound()

    for i in range(20):
        robot.move(-60,-60,0)
        time.sleep(0.3)
        robot.play_recharge_sound()

        
