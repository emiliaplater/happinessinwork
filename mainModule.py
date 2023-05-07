import cv2
import matplotlib.pyplot as plt
import time
# Modules
from Modules.performance.binaryModule import binaryModule
from Modules.algorithms.algorithmModule1 import algorithmModule1
from Modules.algorithms.algorithmModule2 import algorithmModule2
from Modules.calculating.calculateModule import calculateModule



class MainModule:
    def __init__(self, flv_path, time_frame):
        self.flv_path = flv_path
        self.time_frame = time_frame
        
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Time')


    def play(self):
        capture = cv2.VideoCapture(self.flv_path)

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

            timestamp = time.time()

            if left_eye_average_X is not None:
                self.ax.scatter(left_eye_average_X, left_eye_average_Y, timestamp, marker='o', color='blue')
            if right_eye_average_X is not None:
                self.ax.scatter(right_eye_average_X, right_eye_average_Y, timestamp, marker='o', color='blue')

            plt.pause(0.001)


            height, width = frame.shape[:2]
            half_width = width // 2
            left_frame = frame[:, :half_width]
            right_frame = frame[:, half_width:]

            # cv2.imshow('Both', frame)
            cv2.imshow('Left', left_frame)
            cv2.imshow('Right', right_frame)


            key = cv2.waitKey(self.time_frame) & 0xFF
            if key == ord('q'):
                break


        capture.release()
        cv2.destroyAllWindows()


video_player = MainModule('./vids/vid1.flv', 1) # prodive a path
video_player.play()