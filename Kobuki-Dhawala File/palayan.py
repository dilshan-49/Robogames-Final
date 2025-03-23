import cv2
import numpy as np
import time
from kobukidriver import Kobuki
import threading

class BlueBoxFollower:
    def __init__(self):
        self.robot = Kobuki()
        self.cap = cv2.VideoCapture(0)
        self.direction = "Stop"
        self.running = True
        self.last_detection_time = time.time()
        self.timeout = 2  # seconds to stop if no blue detected

    def detect_blue_box(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define blue color range
        blue_lower = np.array([100, 100, 100])  # Light blue
        blue_upper = np.array([140, 255, 255])
        
        mask = cv2.inRange(hsv, blue_lower, blue_upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        blue_detected = False
        
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Adjust area threshold as needed
                blue_detected = True
                self.last_detection_time = time.time()
                
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, "Blue Box", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Determine position
                frame_center = frame.shape[1] // 2
                box_center = x + w // 2
                
                if box_center < frame_center - 50:
                    self.direction = "Left"
                elif box_center > frame_center + 50:
                    self.direction = "Right"
                else:
                    self.direction = "Forward"
                
                cv2.putText(frame, self.direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                break
        
        # If no blue detected for a while, stop the robot
        if not blue_detected:
            if time.time() - self.last_detection_time > self.timeout:
                self.direction = "Stop"
                cv2.putText(frame, "No blue detected - Stopped", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        return frame

    def control_robot(self):
        while self.running:
            if self.direction == "Forward":
                self.robot.move(80, 80, 0)  # Move forward
            elif self.direction == "Left":
                self.robot.move(40, 80, 0)  # Turn left
            elif self.direction == "Right":
                self.robot.move(80, 40, 0)  # Turn right
            elif self.direction == "Stop":
                self.robot.move(0, 0, 0)  # Stop
            
            time.sleep(0.1)  # Small delay to prevent CPU hogging

    def run(self):
        # Start robot control in a separate thread
        robot_thread = threading.Thread(target=self.control_robot)
        robot_thread.daemon = True
        robot_thread.start()
        
        # Play sound to indicate start
        self.robot.play_on_sound()
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = self.detect_blue_box(frame)
                
                cv2.imshow("Blue Box Tracking", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            # Clean up
            self.running = False
            self.robot.move(0, 0, 0)  # Stop the robot
            self.robot.play_off_sound()
            self.cap.release()
            cv2.destroyAllWindows()
            # Wait for the robot thread to finish
            robot_thread.join(timeout=1.0)

def main():
    follower = BlueBoxFollower()
    follower.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")