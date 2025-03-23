import cv2
import numpy as np
import time
from kobukidriver import Kobuki
import threading

isrecover=False

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
        if(isrecover):
            robot_thread.join(timeout=1.0)  
            stop()
            break

def record():
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()

    for i in range(5):
        filename = f"video_clip_{i+1}.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

        print(f"Recording video {i+1}...")
        start_time = time.time()
        while time.time() - start_time < 30:  # Record for 30 seconds
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break
            out.write(frame)
            cv2.imshow('Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.release()
        print(f"Video {i+1} saved as {filename}")

    isrecover=True
    cap.release()
    cv2.destroyAllWindows()
    print("All videos recorded and saved.")

if __name__ == "__main__":
    robot = Kobuki()

    robot_thread = threading.Thread(target=turnRound)
    robot_thread.daemon = True
    robot_thread.start()

    robot.play_on_sound()

    record()




    
