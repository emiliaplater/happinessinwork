import os
import cv2
import csv
import time
# import requests
# from threading import Thread
import matplotlib.pyplot as plt
# from server import VideoUploader
from Modules.performance.binaryModule import binaryModule
from Modules.algorithms.algorithmModule1 import algorithmModule1
from Modules.algorithms.algorithmModule2 import algorithmModule2
from Modules.calculating.calculateModule import calculateModule
from utils.savings.video_saver import VideoSaver
from utils.savings.figure_saver import FigureSaver
from utils.savings.coords_saver import CoordinatesSaver


class MainModule:
    def __init__(
            self, 
            flv_path, 
            wait_key, 
            marker='o', 
            color='blue', 
            output_folder='./output_videos', 
            output_frame_rate=30.0, 
            output_figure_coords_path='./output_videos/'):
        self.flv_path = flv_path
        self.wait_key = wait_key
        self.marker = marker
        self.color = color
        self.output_folder = output_folder
        self.output_frame_rate = output_frame_rate
        self.output_figure_coords_path = output_figure_coords_path

        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Time')

        self.video_saver = VideoSaver(output_folder=self.output_folder)
        self.figure_saver = FigureSaver(output_folder=self.output_figure_coords_path)
        self.coordinates_saver = CoordinatesSaver(output_folder=self.output_figure_coords_path)
        self.left_eye_coords = []
        self.right_eye_coords = []


    def play(self):
        video_name = os.path.splitext(os.path.basename(self.flv_path))[0] 

        capture = cv2.VideoCapture(self.flv_path)

        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = self.output_frame_rate
        left_eye_coords = []
        right_eye_coords = []

        self.video_writer, self.left_video_writer, self.right_video_writer = self.video_saver.initialize_video_writer(
            self.output_folder, frame_width, frame_height, frame_rate, video_name
        )

        while True:
            ret, frame = capture.read()
            if ret is False:
                break

            threshold_frame = binaryModule(frame)

            left_eye_coords1, right_eye_coords1 = algorithmModule1(threshold_frame, frame)
            left_eye_coords2, right_eye_coords2 = algorithmModule2(threshold_frame, frame)

            left_eye_average_X, left_eye_average_Y, right_eye_average_X, right_eye_average_Y, right_eye_average_R, left_eye_average_R = calculateModule(
                left_eye_coords1,
                right_eye_coords1,
                left_eye_coords2,
                right_eye_coords2
            )

            timestamp = time.time()

            if left_eye_average_X and left_eye_average_Y and left_eye_average_R is not None:
                self.ax.scatter(left_eye_average_X, left_eye_average_Y, timestamp, marker=self.marker, color=self.color)
                left_eye_coords.append([left_eye_average_X, left_eye_average_Y, left_eye_average_R])
            if right_eye_average_X and right_eye_average_Y and right_eye_average_R is not None:
                self.ax.scatter(right_eye_average_X, right_eye_average_Y, timestamp, marker=self.marker, color=self.color)
                right_eye_coords.append([right_eye_average_X, right_eye_average_Y, right_eye_average_R])


            height, width = frame.shape[:2]
            half_width = width // 2
            left_frame = frame[:, :half_width]
            right_frame = frame[:, half_width:]

            cv2.imshow('Both', frame)
            cv2.imshow('Left', left_frame)
            cv2.imshow('Right', right_frame)

            self.video_saver.record_frame(self.video_writer, self.left_video_writer, self.right_video_writer, frame)

            key = cv2.waitKey(self.wait_key) & 0xFF
            if key == ord('q'):
                break

        self.figure_saver.save_figure(video_name, self.ax)
        self.coordinates_saver.save_coordinates(video_name, left_eye_coords, right_eye_coords)


        capture.release()
        cv2.destroyAllWindows()

        self.video_saver.release_video_writer(self.video_writer, self.left_video_writer, self.right_video_writer)



video_player = MainModule('./input_videos/vid1.mp4', 1)
video_player.play()


# if __name__ == '__main__':
    # uploader = VideoUploader()
    
    # server_thread = Thread(target=uploader.run)
    # server_thread.start()

    # time.sleep(2)

    # while uploader.uploaded_file is None:
    #     time.sleep(1)


    # uploaded_video_file = uploader.uploaded_file
    # local_video_file_path = f'./{uploaded_video_file}'

    # video_player = MainModule(local_video_file_path, 1)
    # video_player.play()

    # server_thread.join()


    