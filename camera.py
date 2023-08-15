import cv2 as cv

class Camera:

    def __init__(self):
        self.video = cv.VideoCapture(0)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", 0)
        
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                return cv.flip(cv.cvtColor(frame, cv.COLOR_BGR2RGB),1)
            else:   
                return None
        return None
        