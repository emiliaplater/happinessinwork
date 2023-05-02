import unittest
import cv2
from Modules.performance.binaryModule import binaryModule
from Modules.algorithms.algorithmModule1 import algorithmModule1
from Modules.algorithms.algorithmModule2 import algorithmModule2
from Modules.calculating.calculateModule import calculateModule
from mainModule import MainModule



class TestMainModule(unittest.TestCase):
    
    def test_integration(self):
        flv_path = '#'
        time_frame = 1
        video_player = MainModule(flv_path, time_frame)
        
        capture = cv2.VideoCapture(flv_path)
        while True:
            ret, frame = capture.read()
            if ret is False:
                break

            threshold_frame = binaryModule(frame)

            left_eye_coords1, right_eye_coords1 = algorithmModule1(threshold_frame, frame)
            left_eye_coords2, right_eye_coords2 = algorithmModule2(threshold_frame, frame)
            
            left_eye_average_X, left_eye_average_Y, right_eye_average_X, right_eye_average_Y = calculateModule(
                left_eye_coords1, 
                right_eye_coords1, 
                left_eye_coords2, 
                right_eye_coords2
            )

            if left_eye_average_X is not None:
                self.assertIsInstance(left_eye_average_X, float)
            if left_eye_average_Y is not None:
                self.assertIsInstance(left_eye_average_Y, float)
            if right_eye_average_X is not None:
                self.assertIsInstance(right_eye_average_X, float)
            if right_eye_average_Y is not None:
                self.assertIsInstance(right_eye_average_Y, float)

            key = cv2.waitKey(time_frame) & 0xFF
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()