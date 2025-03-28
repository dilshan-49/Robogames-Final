import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("weights/robogames_final.tflite")


isGrabed = False
grab_area = [200,300,450,580] # x1, y1, x2, y2
pixel_distance = 0
objectPresent = False
color = "Unknown"

#found target variables
target_found = False
target_pixel_distance = 0
can_place = False

# Define HSV color ranges
COLOR_RANGES_HSV = {
    "Red": [(0,40,80), (10, 255, 255)],   # Red can also be (170,255,255) in OpenCV
    "Green": [(35, 40, 80), (80, 255, 255)],
    "Blue": [(80, 40, 80), (130, 255, 255)],  #Should change to light blue
    "Yellow": [(20, 40, 80), (35, 255, 255)]
}



# Function to classify color using HSV ranges
def classify_color_hsv(hsv):
    H, S, V = hsv
    for color, (lower, upper) in COLOR_RANGES_HSV.items():
        if lower[0] <= H <= upper[0] and lower[1] <= S <= upper[1] and lower[2] <= V <= upper[2]:
            return color
    return "Unknown"

# Function to detect color in a selected region using HSV
def detect_color_hsv(box, frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV
    max_x1, max_y1, max_x2, max_y2=map(int,box.xyxy[0])
    color_box = hsv_frame[max_y1:max_y2, max_x1:max_x2]

    avg_color_per_row = np.mean(color_box, axis=0)
    avg_color = np.mean(avg_color_per_row, axis=0)
    
    avg_color = np.uint8(avg_color)  # Convert to uint8 (0-255)
    
    detected_color = classify_color_hsv(avg_color)
    
    return avg_color, detected_color  # Return both HSV color and detected color


# Function to check if the object is in the grab area
def is_grab(max_x_center, max_y_center):
    if grab_area[0] < max_x_center < grab_area[2] and grab_area[1] < max_y_center < grab_area[3]:
        return True
    return False

def predict_frame(frame):  
    # Run inference
    
    global isGrabed
    global pixel_distance
    global objectPresent
    detected_color="unknown"
    
    results = model(frame,conf = 0.7)
    result=results[0]
    print(result.verbose())
    result=results[0].cpu().numpy()
    
   
    # Process & display output
    annotated_frame = results[0].plot()


    frame_width = frame.shape[1]
    mid_vertical_line = frame_width//2

    max_box = None
    max_area = 0
    
    for box in result.boxes:
        print(f"xywh : {box.xywh}")
        object_type=int(box.cls[0])
        x_center,y_center,w,h = box.xywh[0]
        pixel_area=w*h
        print(f" class : {box.cls[0]}")
        print(box.cls.shape)
        if pixel_area > max_area:
            max_area = pixel_area
            max_box = box
            
            cv2.putText(annotated_frame, f"Area: {pixel_area:.2f}px", (int(x_center), int(y_center) + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(annotated_frame, (int(grab_area[0]), int(grab_area[1])), (int(grab_area[2]), int(grab_area[3])), (255, 255, 255), 1)

        if max_box is None:
            objectPresent = False
            continue
        else:
            objectPresent = True
            max_x_center,  max_y_center,*_ = max_box.xywh[0]

            pixel_distance =  max_x_center - mid_vertical_line

            avg_color,detected_color = detect_color_hsv(box,frame)
            
            print(f"Detected color: {detected_color}")  

            if is_grab(max_x_center, max_y_center):
                isGrabed = True
                cv2.putText(annotated_frame, "Object in grab area!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Color: {detected_color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  
            else:
                isGrabed = False
                cv2.putText(annotated_frame, "Object not in grab area!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(annotated_frame, f"Color: {detected_color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        cv2.circle(annotated_frame, (int(max_x_center), int(max_y_center)), 5, (0, 255, 0), -1)
        cv2.putText(annotated_frame, f"Dist: {pixel_distance:.2f}px", (int(max_x_center), int(max_y_center) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Color: {detected_color}", (int(max_x_center), int(max_y_center) + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
        cv2.imshow("Frame", annotated_frame)
    return annotated_frame,objectPresent,isGrabed,pixel_distance,detected_color 

# Find a matching target for grabbed box
def find_target(frame, detected_color):
    global target_found
    global target_pixel_distance
    global can_place 

    tframe_width = frame.shape[1]
    mid_line = tframe_width//2

    results = model(frame,conf= 0.7)
    result=results[0].cpu().numpy()

    for box in result.boxes:
        if(int(box.cls[0])==2):
            
            target_x1, target_y1, target_x2, target_y2 = box.xyxy[0]
            target_pix_area = abs((target_y2-target_y1)*(target_x2-target_x1))
            target_center = (target_x1 + target_x2) // 2
            target_color = detect_color_hsv(box, frame)
            
            if(target_color == detected_color):
                target_found = True
                target_pixel_distance = target_center - mid_line
                if(target_pix_area>100000):
                    can_place = True 
                else:
                    can_place = False
            else:
                target_found = False
                target_pixel_distance = 0
                can_place = False

    return target_found, target_pixel_distance, can_place

                



    
cap = cv2.VideoCapture("output.avi")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    find_target(frame, detected_color="Red")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
