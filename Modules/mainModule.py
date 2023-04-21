import cv2
#modules
from binaryModule import binaryModule



class MainModule:
    def __init__(self, flv_path, time_frame):
        self.flv_path = flv_path
        self.time_frame = time_frame

    def play(self):
        capture = cv2.VideoCapture(self.flv_path)

        while True:
            ret, frame = capture.read()
            if ret is False:
                break

            binaryModule(frame)

            cv2.imshow('Frame', frame)

            key = cv2.waitKey(self.time_frame) & 0xFF
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()


video_player = MainModule('#', 50) # prodive a path
video_player.play()