import cv2
import numpy as np
from ultralytics import YOLO
from kobukidriver import Kobuki

# Initialization
model = YOLO("weights/best_float32.tflite")
robot=Kobuki()
cap = cv2.VideoCapture(0)

def contour_area(x1,y1,x2,y2):
    return abs(x2-x1)*abs(y2-y1)

def search_for_boxes():
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Could not read frame")
            return

  
    # Run inference
    result = model(frame,conf = 0.7)[0]

    if result is None:
        print("No Boxes Found!")
    return result

def move_to_box(result):
    # Process & display output
    annotated_frame = result.plot()

def look_around():
    pass

def go_to_box(result):
    max_box = None
    max_area = 0
    print(result)
    for box in result.boxes:
        x,y,w,h = box.xywh.numpy()
        x_center = (x1 + x2) // 2
        y_center = (y1 + y2) // 2
        pixel_area = contour_area(x1,y1,x2,y2)
        print('box:',box)
        if pixel_area > max_area:
            max_area = pixel_area
            max_box = box
            

        if max_box is None:
            continue
        else:
            max_x1, max_y1,max_x2,max_y2 = max_box.xyxy[0].cpu().numpy()
            max_x_center = (max_x1 + max_x2) // 2
            max_y_center = (max_y1 + max_y2) // 2
            pixel_distance = abs(mid_vertical_line - max_x_center)
                
        cv2.circle(annotated_frame, (int(max_x_center), int(max_y_center)), 5, (0, 255, 0), -1)
        cv2.putText(annotated_frame, f"Dist: {pixel_distance:.2f}px", (int(max_x_center), int(max_y_center) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("YOLOv8 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    while True:
        result = search_for_boxes()
        frame_hieght, frame_width, _ = frame.shape
        mid_vertical_line = frame_width//2  

        if result:
            move_to_box(result)
        else:
            look_around()
          
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        