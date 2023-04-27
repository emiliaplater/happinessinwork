import cv2
import numpy as np
#modules
from binaryModule import binaryModule
from algorithmModule1 import algorithmModule1
from algorithmModule2 import algorithmModule2



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

            threshold_frame = binaryModule(frame)

            left_eye_coords1, right_eye_coords1 = algorithmModule1(threshold_frame, frame)
            left_eye_coords2, right_eye_coords2 = algorithmModule2(threshold_frame, frame)
 

            if left_eye_coords1 is not None and left_eye_coords2 is not None:
                left = np.array([left_eye_coords1[0], left_eye_coords2[0]]).mean()
                print('\033[96m' + f'Left eye coordinates: {left}')
            if right_eye_coords1 is not None and right_eye_coords2 is not None:
                right = np.array([right_eye_coords1[0], right_eye_coords2[0]]).mean()
                print('\033[94m' + f'Right eye coordinates: {right}')
            else:
                print('\033[93mNo eye detected...\033[0m')

            height, width = frame.shape[:2]
            half_width = width // 2
            left_frame = frame[:, :half_width]
            right_frame = frame[:, half_width:]

            cv2.imshow('Both', frame)
            cv2.imshow('Left', left_frame)
            cv2.imshow('Right', right_frame)


            key = cv2.waitKey(self.time_frame) & 0xFF
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()


video_player = MainModule('#', 1) # prodive a path
video_player.play()