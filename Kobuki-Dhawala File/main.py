import cv2
import numpy as np
import kobukidriver as kd

def open_camera():
    """Opens the webcam and returns the VideoCapture object."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    return cap

def move_forward():
    """Moves the Kobuki robot forward."""
    kobuki = kd.Kobuki(port="/dev/ttyUSB0")  # Change port if needed

    kobuki.move(0.2, 0)  # Move forward at 0.2 m/s
    kd.time.sleep(2)  # Move for 2 seconds
    kobuki.move(0, 0)  # Stop the robot

    kobuki.close()

def get_color_name(b, g, r):
    """Determines the name of a color based on BGR values."""
    colors = {
        "Red": [(0, 0, 100), (100, 100, 255)],
        "Green": [(0, 100, 0), (100, 255, 100)],
        "Blue": [(200, 200, 100), (255, 255, 150)],
        "Yellow": [(100, 100, 0), (255, 255, 100)],
    }

    for color, (lower, upper) in colors.items():
        if all(lower[i] <= val <= upper[i] for i, val in enumerate([b, g, r])):
            return color
    return "Unknown"

def detect_color(frame):
    """Detects the color at the center of the frame and prints it."""
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2

    # Get the BGR color of the center pixel
    region_size = 10
    region = frame[center_y - region_size // 2:center_y + region_size // 2,
                   center_x - region_size // 2:center_x + region_size // 2]

    # Calculate the average BGR color of the region
    b, g, r = np.mean(region, axis=(0, 1)).astype(int)    
    print(f"Detected Color at Center: B={b}, G={g}, R={r}")
    # Get color name
    color_name = get_color_name(b, g, r)
    
    
    print(f"Detected Color at Center: {color_name}")

    # Draw a circle at the center
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 0), -1)
    cv2.putText(frame, color_name, (center_x - 50, center_y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    return frame

def main():
    move_forward()
    cap = open_camera()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        frame = detect_color(frame)

        cv2.imshow("Camera Feed", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
