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
from utils.savings.video_saver import initialize_video_writer, record_frame, release_video_writer




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

        self.video_writer = None



    def save_figure(self, video_name):
        details_folder = os.path.join(self.output_figure_coords_path, f'details_for_{video_name}')
        os.makedirs(details_folder, exist_ok=True)

        graphic_coords_folder = os.path.join(details_folder, f'graphic&coords_{video_name}')
        os.makedirs(graphic_coords_folder, exist_ok=True)

        graphic_folder = os.path.join(graphic_coords_folder, 'graphic')
        os.makedirs(graphic_folder, exist_ok=True)
        graphic_path = os.path.join(graphic_folder, f'graphic_{video_name}.png')


        self.ax.figure.savefig(graphic_path)


    def save_coordinates(self, video_name, left_eye_coords, right_eye_coords):
        details_folder = os.path.join(self.output_figure_coords_path, f'details_for_{video_name}')
        os.makedirs(details_folder, exist_ok=True)

        graphic_coords_folder = os.path.join(details_folder, f'graphic&coords_{video_name}')
        os.makedirs(graphic_coords_folder, exist_ok=True)

        coordinates_folder = os.path.join(graphic_coords_folder, 'coordinates')
        os.makedirs(coordinates_folder, exist_ok=True)
        coordinates_file_path = os.path.join(coordinates_folder, f'coordinates_{video_name}.csv')

        with open(coordinates_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for i in range(len(left_eye_coords)):
                if left_eye_coords[i] is not None:
                    x1, y1, r1 = left_eye_coords[i]
                    writer.writerow(['Left eye\'s coordinates: ' + f'X: {x1}', f' Y: {y1}', f' R: {r1}'])
                else:
                    writer.writerow('No eye detected...')
            
            for i in range(len(right_eye_coords)):
                if right_eye_coords[i] is not None:
                    x2, y2, r2 = right_eye_coords[i]
                    writer.writerow(['Right eye\'s coordinates: ' + f'X: {x2}', f' Y: {y2}', f' R: {r2}'])
                else:
                    writer.writerow('No eye detected...')


    def play(self):
        video_name = os.path.splitext(os.path.basename(self.flv_path))[0] 

        capture = cv2.VideoCapture(self.flv_path)

        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = self.output_frame_rate
        left_eye_coords = []
        right_eye_coords = []

        self.video_writer, self.left_video_writer, self.right_video_writer = initialize_video_writer(
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

            plt.pause(0.001)

            height, width = frame.shape[:2]
            half_width = width // 2
            left_frame = frame[:, :half_width]
            right_frame = frame[:, half_width:]

            cv2.imshow('Both', frame)
            cv2.imshow('Left', left_frame)
            cv2.imshow('Right', right_frame)

            record_frame(self.video_writer, self.left_video_writer, self.right_video_writer, frame)

            release_video_writer(self.video_writer, self.left_video_writer, self.right_video_writer)

            key = cv2.waitKey(self.wait_key) & 0xFF
            if key == ord('q'):
                break

        self.save_figure(video_name)
        self.save_coordinates(video_name, left_eye_coords, right_eye_coords)

        capture.release()
        cv2.destroyAllWindows()


video_player = MainModule('./input_videos/vid1.flv', 1)
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


    