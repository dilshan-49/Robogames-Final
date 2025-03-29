import cv2
import numpy as np
import csv
import os

colorArray=["Blue","Red","Green","Yellow"]
def makeFrames(cap):
        ret, frame = cap.read()
        if ret:
                
            height, width, _ = frame.shape
            box_size = 200  # Size of the central box
            x_center, y_center = width // 2, height // 2
            x1, y1 = x_center - box_size // 2, y_center - box_size // 2
            x2, y2 = x_center + box_size // 2, y_center + box_size // 2
            
            # Draw the center box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Extract the region of interest (ROI) and convert to HSV
            roi = frame[y1:y2, x1:x2]
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # Calculate the average HSV value inside the box
            avg_hsv = np.mean(hsv_roi, axis=(0, 1))
            
            # Display HSV values on the frame
            text = f"H: {int(avg_hsv[0])}, S: {int(avg_hsv[1])}, V: {int(avg_hsv[2])}"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show the frame
            cv2.imshow("Camera Feed", frame)
            return frame,avg_hsv
        else:
            return None,None

def main():
    cap = cv2.VideoCapture(0)  # Open the default camera
    csv_file = "captured_data.csv"
    
    # Create CSV file if it doesn't exist
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Filename", "H", "S", "V","Color"])

    while True:
        frame,avg_hsv=makeFrames(cap)
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if cv2.waitKey(10) & 0xFF == ord('p'):
            if(len(colorArray)!=0):
                color=colorArray.pop(0)
                filename = f"screenshot_{color}.png"
                cv2.imwrite(filename, frame)
                
                # Append data to CSV file
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([filename, int(avg_hsv[0]), int(avg_hsv[1]), int(avg_hsv[2]),color])
                    print(f"Screenshot saved as {filename}")
            else:
                print("All Taken !")   
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
