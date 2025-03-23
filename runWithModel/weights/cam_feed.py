import cv2
from threading import Thread


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Error: Unable to access the camera.")
        self.ret, self.frame = self.cap.read()
        self.running = True
        self.thread = Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.cap.read()

    def get_frame(self):
        if self.ret:
            return self.frame
        return None
    
    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()
