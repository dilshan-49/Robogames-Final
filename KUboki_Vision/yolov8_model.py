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

COLOR_RANGES_RGB ={
    "Red": [(150, 90, 100), (255, 130, 255)],
    "Green": [(60, 100, 0), (90, 255, 100)],
    "Blue": [(50, 120, 150), (120, 200, 255)],
    "Yellow": [(150, 150, 80), (255,255,110)]
}


# Function to classify color using HSV ranges
def classify_color_hsv(hsv):
    H, S, V = hsv
    for color, (lower, upper) in COLOR_RANGES_HSV.items():
        if lower[0] <= H <= upper[0] and lower[1] <= S <= upper[1] and lower[2] <= V <= upper[2]:
            return color
    return "Unknown"


def get_dominant_color_hsv(hsv_box):
    
    # Flatten the hue channel
    hue_values = hsv_box[:, :, 0].flatten()

    # Calculate the histogram of hue values (0-179 for HSV)
    hist = np.bincount(hue_values, minlength=180)

    # Find the hue with the maximum count
    dominant_hue = np.argmax(hist)

    return dominant_hue


def detect_target_color_hsv(box, frame):
   
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    max_x1, max_y1, max_x2, max_y2 = map(int, box.xyxy[0])
    hsv_box = hsv_frame[max_y1:max_y2, max_x1:max_x2]

    # Get the dominant hue value
    dominant_hue = get_dominant_color_hsv(hsv_box)

    # Map the dominant hue to a color name
    detected_color = classify_color_hsv([dominant_hue, 255, 255])

    return detected_color

def classify_color_rgb(rgb):
    R, G, B = rgb
    for color, (lower, upper) in COLOR_RANGES_RGB.items():
        if lower[0] <= R <= upper[0] and lower[1] <= G <= upper[1] and lower[2] <= B <= upper[2]:
            return color
    return "Unknown"

def get_dominant_rgb_color(rgb_box):
    """Finds the most frequent RGB color in the region."""
    reshaped = rgb_box.reshape(-1, 3)  # Flatten into (R, G, B) list
    unique_colors, counts = np.unique(reshaped, axis=0, return_counts=True)
    dominant_rgb = unique_colors[np.argmax(counts)]  # Get the most common color
    return tuple(dominant_rgb)  # Return as (R, G, B)


def detect_target_color_rgb(box, frame):
    """Detects the dominant color inside the bounding box of an object."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    max_x1, max_y1, max_x2, max_y2 = map(int, box.xyxy[0])
    rgb_box = rgb_frame[max_y1:max_y2, max_x1:max_x2]

    # Get the dominant RGB color
    dominant_rgb = get_dominant_rgb_color(rgb_box)

    # Classify the dominant RGB color to a single named color
    detected_color = classify_color_rgb(dominant_rgb)
    print(f"Detected RGB: {dominant_rgb}")
    print(f"Detected color: {detected_color}")
    return detected_color  # Returns both name & RGB values

# Function to check if the object is in the grab area
def is_grab(max_x_center, max_y_center):
    if grab_area[0] < max_x_center < grab_area[2] and grab_area[1] < max_y_center < grab_area[3]:
        return True
    return False

# Function to check if two rectangles intersect
def has_intersection(grab_area, box_area):
    # Extract coordinates
    grab_x1, grab_y1, grab_x2, grab_y2 = grab_area
    box_x1, box_y1, box_x2, box_y2 = box_area

    # Calculate the intersection rectangle
    inter_x1 = max(grab_x1, box_x1)
    inter_y1 = max(grab_y1, box_y1)
    inter_x2 = min(grab_x2, box_x2)
    inter_y2 = min(grab_y2, box_y2)

    # Check if the intersection rectangle has a positive area
    if inter_x1 < inter_x2 and inter_y1 < inter_y2:
        return True  # Intersection exists
    return False  # No intersection

# Function to predict the frame and display results
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

            detected_color = detect_target_color_hsv(box,frame)
            
            print(f"Detected color: {detected_color}")  

            if is_grab(max_x_center, max_y_center):
                isGrabed = True
                cv2.putText(annotated_frame, "Object in grab area!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.putText(annotated_frame, f"Color: {detected_color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  
            else:
                isGrabed = False
                cv2.putText(annotated_frame, "Object not in grab area!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if(detected_color != "Unknown"):
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

    annotated_frame = results[0].plot()
    cv2.rectangle(annotated_frame, (int(grab_area[0]), int(grab_area[1])), (int(grab_area[2]), int(grab_area[3])), (255, 0, 0), 2)
    for box in result.boxes:
        if(int(box.cls[0])==2):
            
            target_x1, target_y1, target_x2, target_y2 = box.xyxy[0]
            target_pix_area = abs((target_y2-target_y1)*(target_x2-target_x1))
            target_center = (target_x1 + target_x2) // 2
            target_color = detect_target_color_rgb(box, frame)

            cv2.putText(annotated_frame, f"Target Color: {target_color}", (int(target_x1), int(target_y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Dist: {target_pixel_distance:.2f}px", (int(target_x1), int(target_y1) + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Area: {target_pix_area:.2f}px", (int(target_x1), int(target_y1) + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            if(target_color == detected_color):
                target_found = True
                target_pixel_distance = target_center - mid_line
                
                if(target_pix_area>100000 and has_intersection(grab_area, box.xyxy[0])):
                    can_place = True 
                    cv2.putText(annotated_frame, "Target Found!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"Target Color: {target_color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    can_place = False
            else:
                target_found = False
                target_pixel_distance = 0
                can_place = False
    cv2.imshow("Frame", annotated_frame)          
    return target_found, target_pixel_distance, can_place

                



cap = cv2.VideoCapture("robogames01.mp4")

# Define the codec and create VideoWriter object
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
output_file = "annotated_video.mp4"

# Use the MP4V codec for saving the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Predict and display the frame
    annotated_frame, objectPresent, isGrabed, pixel_distance, detected_color = predict_frame(frame)
    
    # Write the annotated frame to the output video
    out.write(annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()
