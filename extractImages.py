###########################################################
###   Extract images from videos to make the dataset    ###
###########################################################

import cv2
import os
import numpy as np
import glob

video= glob.glob("E:\\RoboGames\\train-vid\\train\\*.avi")

# Path to the input video
output_dir = "E:\\RoboGames\\Robogames-Final\\datasets\\train_images"  # Directory to save the extracted images
os.makedirs(output_dir, exist_ok=True)
frame_count = 0
print(video)
for video_path in video:
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        exit()
    frame_skip = 10
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or cannot read frame.")
            break
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue    
        # Get original frame dimensions


        # Save the padded frame as an image
        name=frame_count//frame_skip
        output_path = os.path.join(output_dir, f"frame_{name:04d}.jpg")
        cv2.imwrite(output_path, frame)
        frame_count += 1

        # Optional: Display the frame (for debugging)
        # cv2.imshow('Frame', padded_frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()
cv2.destroyAllWindows()

print(f"Extracted {frame_count} frames and saved to {output_dir}")