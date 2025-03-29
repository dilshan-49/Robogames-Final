import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("model/robogames_v2.pt")


isGrabed = False
grab_area = [200,370,440,480] # x1, y1, x2, y2
pixel_distance = 0
objectPresent = False
color = "Unknown"
colorArray = ["Yellow", "Green", "Red", "Red"]


#found target variables
target_found = False
target_pixel_distance = 0
can_place = False

COLOR_RANGES_RGB ={
    "Red": [(150, 90, 100), (255, 130, 255)],
    "Green": [(60, 100, 0), (90, 255, 100)],
    "Blue": [(50, 120, 150), (120, 200, 255)],
    "Yellow": [(150, 150, 80), (255, 255, 110)]
}


COLOR_RANGES_HSV = {
    "Red": [(0,40,80), (10, 255, 255)],   # Red can also be (170,255,255) in OpenCV
    "Green": [(35, 40, 80), (80, 255, 255)],
    "Blue": [(80, 40, 80), (130, 255, 255)],  #Should change to light blue
    "Yellow": [(20, 40, 80), (35, 255, 255)],
    "White" : [(0, 0, 200), (180, 30, 255)]
}

def classify_color_rgb(rgb):
    R, G, B = rgb
    print(f"R : {R},  G : {G} ,  B:{B}")
    for color, (lower, upper) in COLOR_RANGES_RGB.items():
        if lower[0] <= R <= upper[0] and lower[1] <= G <= upper[1] and lower[2] <= B <= upper[2]:
            return color
    return "Unknown"

def get_dominent_rgb_colr(rgb_box):

    pixels = rgb_box.reshape(-1, 3)
    
    # Count unique RGB values
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Find the most frequent RGB color
    dominant_rgb = unique_colors[np.argmax(counts)]
    
    return tuple(dominant_rgb)  

def detect_target_color_rgb(box, frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    max_x1, max_y1, max_x2, max_y2 = map(int, box.xyxy[0])
    rgb_box = rgb_frame[max_y1:max_y2, max_x1:max_x2]

    # Get the dominant hue value
    dominant_rgb = get_dominent_rgb_colr(rgb_box)
    cv2.putText(frame, f"Dominant RGB: {dominant_rgb[0]},{dominant_rgb[1]},{dominant_rgb[2]} ", (max_x2, max_y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Map the dominant hue to a color name
    detected_color = classify_color_rgb(dominant_rgb)

    return detected_color

# Function to classify color using HSV ranges
def classify_color_hsv(hsv):
    H, S, V = hsv
    for color, (lower, upper) in COLOR_RANGES_HSV.items():
        if (lower[0] <= H <= upper[0]):
            return color
    return "Unknown"


def get_dominant_color_hsv(hsv_box):
    """
    Get the most available (dominant) color in an HSV NumPy array.

    Args:
        hsv_box (numpy.ndarray): The HSV region of interest (ROI).

    Returns:
        int: The dominant hue value (0-179).
    """
    # Flatten the hue channel
    hue_values = hsv_box[:, :, 0].flatten()

    # Calculate the histogram of hue values (0-179 for HSV)
    hist = np.bincount(hue_values, minlength=180)

    # Find the hue with the maximum count
    dominant_hue = np.argmax(hist)

    return dominant_hue

def detect_dominant_color_hsv(box, frame):
    """
    Detect the dominant color in a bounding box using HSV.

    Args:
        box: The bounding box object from YOLO.
        frame: The current frame in BGR format.

    Returns:
        int: The dominant hue value (0-179).
        str: The detected color name.
    """
    # Convert the frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Extract the bounding box coordinates
    max_x1, max_y1, max_x2, max_y2 = map(int, box.xyxy[0])

    # Get the HSV region of interest (ROI)
    hsv_box = hsv_frame[max_y1:max_y2, max_x1:max_x2]

    # Get the dominant hue value
    dominant_hue = get_dominant_color_hsv(hsv_box)

    # Map the dominant hue to a color name
    detected_color = classify_color_hsv([dominant_hue, 255, 255])  # Use max S and V for classification

    return dominant_hue, detected_color

def detect_target_color_hsv(box, frame):
    """
    Detect the dominant color in a bounding box using HSV.

    Args:
        box: The bounding box object from YOLO.
        frame: The current frame in BGR format.

    Returns:
        str: The detected color name.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    max_x1, max_y1, max_x2, max_y2 = map(int, box.xyxy[0])
    hsv_box = hsv_frame[max_y1:max_y2, max_x1:max_x2]

    # Get the dominant hue value
    dominant_hue = get_dominant_color_hsv(hsv_box)
    cv2.putText(frame, f"Dominant hue: {dominant_hue}", (max_x2, max_y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Map the dominant hue to a color name
    detected_color = classify_color_hsv([dominant_hue, 255, 255])

    return detected_color


# Function to check if the object is in the grab area
def is_grab(max_x_center, max_y_center, color):
    if grab_area[0] < max_x_center < grab_area[2] and grab_area[1] < max_y_center < grab_area[3]:
        return True
    return False

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


def search_box(frame):  
    global isGrabed
    global pixel_distance
    global objectPresent
    detected_color="unknown"
    obstacle_dist = 1000
    target_box = None
    # Run inference
    results = model(frame,conf = 0.7)
    result=results[0].cpu().numpy()
  
    annotated_frame = results[0].plot()


    frame_width = frame.shape[1]
    mid_vertical_line = frame_width//2

    target_color=colorArray[-1]
    cv2.putText(annotated_frame, f"Target color : {target_color}", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.rectangle(annotated_frame, (int(grab_area[0]), int(grab_area[1])), (int(grab_area[2]), int(grab_area[3])), (255, 255, 255), 1)
    
    for box in result.boxes:
        object_type=int(box.cls[0])
 
        x_center,y_center,w,h = box.xywh[0]
        detected_color = detect_target_color_hsv(box,frame)
        detected_color2 = detect_target_color_rgb(box,frame)

        if object_type==0: 
            print(f"Detected color: {detected_color}") 
            cv2.putText(annotated_frame, f"Color: {detected_color}", (int(x_center), int(y_center) + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if detected_color == target_color:
                target_x_center=x_center
                target_y_center=y_center
                target_box = box   
            

        elif (object_type==1 and detected_color=="White") :  ## obstacle detected
    
            if (w*h>10000 and 220<x_center<420):
                obstacle_dist=x_center-mid_vertical_line
            pass

    if target_box is None:
        objectPresent = False

        
    else:
        objectPresent = True
        pixel_distance =  target_x_center - mid_vertical_line


        if is_grab(target_x_center, target_y_center,color):
            isGrabed = True
            cv2.putText(annotated_frame, "Object in grab area!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Color: {detected_color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  
        else:
            isGrabed = False
            cv2.putText(annotated_frame, "Object not in grab area!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(annotated_frame, f"Color: {detected_color}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        cv2.circle(annotated_frame, (int(target_x_center), int(target_y_center)), 5, (0, 255, 0), -1)
        cv2.putText(annotated_frame, f"Dist: {pixel_distance:.2f}px", (int(target_x_center), int(target_y_center) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Color: {detected_color}", (int(target_x_center), int(target_y_center) + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

    return annotated_frame,objectPresent,isGrabed,pixel_distance

# Find a matching target for grabbed box
def find_target(frame, detected_color):
    global target_found
    global target_pixel_distance
    global can_place 
    global isGrabed
    print("Searching for target...")
    tframe_width = frame.shape[1]
    mid_line = tframe_width//2

    results = model(frame,conf= 0.7)
    result=results[0].cpu().numpy()
    annotated_frame = results[0].plot()

    for box in result.boxes:
        if(int(box.cls[0])==2):
            
            target_x1, target_y1, target_x2, target_y2 = box.xyxy[0]
            target_pix_area = abs((target_y2-target_y1)*(target_x2-target_x1))
            target_center = (target_x1 + target_x2) // 2
            target_color = detect_target_color_hsv(box, frame)
            target_color2 = detect_target_color_rgb(box, frame)

            cv2.putText(annotated_frame, f"Color: {detected_color}", (int(target_x2), int(target_y2) + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
            print(f"Target color: {target_color}")

            if(target_color == detected_color):
                print("Target found!")
                cv2.rectangle(annotated_frame, (int(target_x1), int(target_y1)), (int(target_x2), int(target_y2)), (0, 255, 0), 2)
                cv2.putText(annotated_frame, "Target found!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                target_found = True
                target_pixel_distance = target_center - mid_line
                if(target_pix_area>100000 and has_intersection(grab_area, box.xyxy[0])):
                    print(" Place the shit")
                    can_place = True
                    isGrabed = False
                else:
                    can_place = False
            else:
                target_found = False
                target_pixel_distance = 0
                can_place = False

    return annotated_frame,target_found, target_pixel_distance, can_place

