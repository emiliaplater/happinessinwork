import os
import matplotlib
matplotlib.use('Agg')
import zipfile
from mainModule import MainModule
from utils.exceptions.exceptions import InvalidVideoFile, NoVideoFileSelected

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'

def process_video_handler(event, context):
    try:
        video_files = event['video']
        if not video_files:
            raise NoVideoFileSelected('No video file selected.')

        video_file = video_files[0]
        video_filename = video_file['filename']

        # Check if the file extension is mp4
        if not video_filename.endswith('.mp4'):
            raise InvalidVideoFile('Invalid video file. Only .mp4 files are allowed.')

        input_videos_folder = '/tmp/input_videos'
        os.makedirs(input_videos_folder, exist_ok=True)

        video_path = os.path.join(input_videos_folder, video_filename)
        with open(video_path, 'wb') as f:
            f.write(video_file['body'])

        video_player = MainModule(video_path, 1, output_folder='/tmp/output_videos')
        video_player.play()

        processed_video_folder = video_player.output_folder

        zip_path = os.path.join(processed_video_folder, f'details_for_{video_player.video_name}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(processed_video_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, processed_video_folder)
                    zipf.write(file_path, arcname)

        with open(zip_path, 'rb') as f:
            output_bytes = f.read()

        os.remove(zip_path)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'attachment; filename=output_folder.zip'
            },
            'body': output_bytes,
            'isBase64Encoded': True
        }

    except NoVideoFileSelected as e:
        return {
            'statusCode': e.status_code,
            'body': {'error': e.message}
        }

    except InvalidVideoFile as e:
        return {
            'statusCode': e.status_code,
            'body': {'error': e.message}
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': 'An unexpected error occurred.'}
        }
