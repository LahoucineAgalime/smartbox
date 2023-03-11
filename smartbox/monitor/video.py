import cv2


class VideoCamera(object):
    def __init__(self, rtsp):
        self.video = None
        self.rtsp = rtsp

    def __del__(self):
        if self.video:
            self.video.release()

    def check_online(self):
        video = cv2.VideoCapture(self.rtsp)
        success = video.read()[0]
        return success

    def get_frame(self):
        image = self.video.read()[1]
        jpeg = cv2.imencode('.jpg', image)[1]
        return jpeg.tobytes()

    def gen(self):
        self.video = cv2.VideoCapture(self.rtsp)
        try:
            while True:
                frame = self.get_frame()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except GeneratorExit:
            pass
