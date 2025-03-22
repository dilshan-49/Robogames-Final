import cv2
import numpy as np
import time
import threading
# from kobukidriver import Kobuki  # Uncomment if using the actual robot

class colorBoxPlacement:
    def __init__(self):
        # self.robot = Kobuki()  # Uncomment when using the robot
        self.cap = cv2.VideoCapture(0)  # Open the default webcam
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit(1)
        
        self.direction = "Stop"
        self.running = True
        self.last_detection_time = time.time()
        self.timeout = 2
        
        # Define HSV color ranges for detection
        self.color_ranges = {
            "Green": [(np.array([35, 100, 100]), np.array([85, 255, 255]))],
            "Yellow": [(np.array([25, 100, 100]), np.array([35, 255, 255]))],
            "Blue": [(np.array([90, 100, 100]), np.array([130, 255, 255]))],
            "Red": [(np.array([0, 100, 100]), np.array([10, 255, 255])),
                     (np.array([170, 100, 100]), np.array([180, 255, 255]))],
            "White": [(np.array([0, 0, 200]), np.array([180, 50, 255]))]
        }
    def initializecolorPositions(self):
        # Set the initial position of the robot
        # self.robot.move(0, 0, 0)
        time.sleep(1)
    def detect_color_boxes(self, frame):
        """Detects multiple colored boxes in the frame, labels them, and returns processed frame."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        for color, ranges in self.color_ranges.items():
            for lower, upper in ranges:
                mask = cv2.inRange(hsv, lower, upper)
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                for cnt in contours:
                    if cv2.contourArea(cnt) > 500:  # Adjust size threshold as needed
                        x, y, w, h = cv2.boundingRect(cnt)
                        
                        # Draw a square around detected colors
                        size = max(w, h)
                        cv2.rectangle(frame, (x, y), (x + size, y + size), (0, 255, 0), 2)
                        
                        # Label the detected color
                        cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame
    
    def control_robot(self):
        """Controls the robot based on detected direction."""
        while self.running:
            if self.direction == "Forward":
                print("Moving Forward")  # self.robot.move(80, 80, 0)
            elif self.direction == "Left":
                print("Turning Left")  # self.robot.move(40, 80, 0)
            elif self.direction == "Right":
                print("Turning Right")  # self.robot.move(80, 40, 0)
            elif self.direction == "Stop":
                print("Stopping")  # self.robot.move(0, 0, 0)
            
            time.sleep(0.1)  # Prevents CPU overuse
    
    def run(self):
        """Main function to capture video and detect colors."""
        # Start robot control in a separate thread
        # robot_thread = threading.Thread(target=self.control_robot)
        # robot_thread.daemon = True
        # robot_thread.start()
        
        # Play sound to indicate start
        # self.robot.play_on_sound()
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Failed to capture image")
                    break
                
                frame = self.detect_color_boxes(frame)
                
                cv2.imshow("Color Box Detection", frame)  # Fixed missing window name
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            # Clean up
            self.running = False
            # self.robot.move(0, 0, 0)  # Stop the robot
            # self.robot.play_off_sound()
            self.cap.release()
            cv2.destroyAllWindows()
            # robot_thread.join(timeout=1.0)  # Uncomment if using threading

def main():

    follower = colorBoxPlacement()
    follower.initializecolorPositions()
    follower.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")