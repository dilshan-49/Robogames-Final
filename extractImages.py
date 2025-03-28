import cv2
import os
import glob

# Path to the videos


# Directory to save the extracted images
output_dir = "E:\\RoboGames\\train_images"
os.makedirs(output_dir, exist_ok=True)

frame_count = 67

video_path="E:\\output.avi"
    # Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Cannot open video file {video_path}.")
    exit()

print(f"Playing video: {video_path}")
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read frame.")
        break

    # Display the frame
    cv2.imshow('Video', frame)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):  # Spacebar pressed
        # Save the current frame
        output_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Saved frame to {output_path}")
        frame_count += 1

    elif key == ord('q'):  # 'q' pressed to quit
        print("Exiting video playback.")
        break

cap.release()

cv2.destroyAllWindows()

print(f"Extracted {frame_count} frames and saved to {output_dir}")