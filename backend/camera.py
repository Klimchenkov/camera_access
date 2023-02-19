from datetime import datetime

import threading

import cv2


class Camera:
    def __init__(self, url):
        self.thread = None
        self.current_frame = None
        self.is_running: bool = False
        self.camera = cv2.VideoCapture(url)
        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.dt_format = "%Y-%m-%d %H:%M:%S"
        self.text_color = (0,164,255)
    
    def __del__(self):
        self.camera.release()
        
    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()
    
    def stop(self):
        self.is_running = False
        self.thread.join()
        self.thread = None
     
    def _capture(self):
        self.is_running = True
        while self.is_running:
            ret, frame = self.camera.read()
            if ret:
                cv2.putText(frame, datetime.now().strftime(self.dt_format), (10,30), self.font, 1, self.text_color, 2, cv2.LINE_AA)
                ret, encoded = cv2.imencode('.jpg', frame)
                if ret:
                    self.current_frame = encoded
                else:
                    print("Failed to encode frame")
            else:
                print("Failed to capture frame")
        print("Reading thread stopped")
        self.thread = None
        self.is_running = False