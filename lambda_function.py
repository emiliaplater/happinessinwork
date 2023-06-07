import os
import zipfile
import json
import boto3
import cv2
import tempfile
from mainModule import MainModule
from utils.exceptions.exceptions import InvalidVideoFile, NoVideoFileSelected
from utils.savings.coords_saver import CoordinatesSaver
from utils.savings.figure_saver import FigureSaver
from utils.savings.video_saver import VideoSaver


def lambda_handler(event, context):
    print(event)

    records = event.get('Records', [])
    if not records:
        raise NoVideoFileSelected('No video file selected.')

    first_record = records[0]
    s3_bucket_name = first_record['s3']['bucket']['name']
    video_filename = first_record['s3']['object']['key']

    s3_client = boto3.client('s3')

    response = s3_client.get_object(Bucket=s3_bucket_name, Key=video_filename)
    video_content = response['Body'].read()

    if not video_filename.endswith('.mp4'):
        raise InvalidVideoFile('Invalid video file. Only .mp4 files are allowed.')

    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_file.write(video_content)
        temp_file_path = temp_file.name

    output_folder = '/tmp/output_videos'
    os.makedirs(output_folder, exist_ok=True)

    video_player = MainModule(temp_file_path, 1, output_folder=output_folder)
    video_player.play()
    os.remove(temp_file_path)

    processed_video_folder = video_player.output_folder
    zip_path = os.path.join(processed_video_folder, f'details_for_{video_filename}.zip')

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(processed_video_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, processed_video_folder)
                zipf.write(file_path, arcname)

    coordinates_saver = CoordinatesSaver(output_folder=output_folder)
    left_eye_coords = video_player.left_eye_coords
    right_eye_coords = video_player.right_eye_coords
    coordinates_saver.save_coordinates(video_filename, left_eye_coords, right_eye_coords)

    figure_saver = FigureSaver(output_folder=output_folder)
    figure_saver.save_figure(video_filename, video_player.figure_module.ax)

    video_saver = VideoSaver(output_folder=output_folder)
    capture = cv2.VideoCapture(temp_file_path)
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = video_player.output_frame_rate
    video_writer, left_video_writer, right_video_writer = video_saver.initialize_video_writer(
        output_folder=output_folder,
        frame_width=frame_width,
        frame_height=frame_height,
        frame_rate=frame_rate,
        video_name=video_filename
    )
    for frame in video_player.get_processed_frames():
        video_saver.record_frame(video_writer, left_video_writer, right_video_writer, frame)
    video_saver.release_video_writer(video_writer, left_video_writer, right_video_writer)

    s3_response = s3_client.put_object(
        Bucket='centroids-viewer',
        Key=f'{video_filename}.zip',
        Body=open(zip_path, 'rb')
    )

    print(s3_response)
    print(f'Name: {video_filename}')
    print('Lambda execution has completed.')

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Lambda execution completed.'})
    }