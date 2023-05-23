import os
import cv2



def initialize_video_writer(output_folder, frame_width, frame_height, frame_rate, video_name):
    details_folder = os.path.join(output_folder, f'details_for_{video_name}', 'screen_frames')
    os.makedirs(details_folder, exist_ok=True)

    screen_main_frame_folder = os.path.join(details_folder, 'main_screen_frame')
    os.makedirs(screen_main_frame_folder, exist_ok=True)
    screen_main_frame_path = os.path.join(screen_main_frame_folder, f'main_frame_{video_name}.flv')

    left_folder = os.path.join(details_folder, f'left_screen_frame')
    os.makedirs(left_folder, exist_ok=True)
    left_video_path = os.path.join(left_folder, f'left_eye_{video_name}.flv')

    right_folder = os.path.join(details_folder, f'right_screen_frame')
    os.makedirs(right_folder, exist_ok=True)
    right_video_path = os.path.join(right_folder, f'right_eye_{video_name}.flv')

    fourcc = cv2.VideoWriter_fourcc(*'FLV1')
    left_fourcc = cv2.VideoWriter_fourcc(*'FLV1')
    right_fourcc = cv2.VideoWriter_fourcc(*'FLV1')

    video_writer = cv2.VideoWriter(screen_main_frame_path, fourcc, frame_rate, (frame_width, frame_height))
    left_video_writer = cv2.VideoWriter(left_video_path, left_fourcc, frame_rate, (frame_width // 2, frame_height))
    right_video_writer = cv2.VideoWriter(right_video_path, right_fourcc, frame_rate, (frame_width // 2, frame_height))

    return video_writer, left_video_writer, right_video_writer


def record_frame(video_writer, left_video_writer, right_video_writer, frame):
    if video_writer is not None:
        video_writer.write(frame)

    if left_video_writer is not None:
        left_frame = frame[:, :frame.shape[1] // 2]
        left_video_writer.write(left_frame)

    if right_video_writer is not None:
        right_frame = frame[:, frame.shape[1] // 2:]
        right_video_writer.write(right_frame)

def release_video_writer(video_writer, left_video_writer, right_video_writer):
    if video_writer is not None:
        video_writer.release()

    if left_video_writer is not None:
        left_video_writer.release()

    if right_video_writer is not None:
        right_video_writer.release()
