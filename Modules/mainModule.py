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

            threshold = binaryModule(frame)

            left_eye_coords1, right_eye_coords1 = algorithmModule1(threshold, frame)
            left_eye_coords2, right_eye_coords2 = algorithmModule2(threshold, frame)

            # Calculate the average of the left and right eye coordinates
            if left_eye_coords1 is not None and left_eye_coords2 is not None:
                left = np.array([left_eye_coords1[0], left_eye_coords2[0]]).mean()
                print('\033[96m' + f'Left eye coordinates: {left}')
            if right_eye_coords1 is not None and right_eye_coords2 is not None:
                right = np.array([right_eye_coords1[0], right_eye_coords2[0]]).mean()
                print('\033[94m' + f'Right eye coordinates: {right}')
            else:
                print('\033[93mNo eye detected...\033[0m')

            cv2.imshow('Frame', frame)

            key = cv2.waitKey(self.time_frame) & 0xFF
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()


video_player = MainModule('../vids/vid2.flv', 50) # prodive a path
video_player.play()