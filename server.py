import os
import zipfile
import tornado.ioloop
import tornado.web
from mainModule import MainModule

class ProcessVideoHandler(tornado.web.RequestHandler):
    def post(self):
        video_file = self.request.files['video'][0]

        input_videos_folder = './input_videos'
        os.makedirs(input_videos_folder, exist_ok=True)

        video_path = os.path.join(input_videos_folder, video_file['filename'])
        with open(video_path, 'wb') as f:
            f.write(video_file['body'])

        video_player = MainModule(video_path, 1, output_folder='./output_videos')
        video_player.play()

        processed_video_folder = video_player.output_folder

        zip_path = os.path.join(processed_video_folder, f'details_for_{video_player.video_name}.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(processed_video_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, processed_video_folder)
                    zipf.write(file_path, arcname)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=output_folder.zip')

        with open(zip_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                self.write(chunk)
                self.flush()

        self.finish()

        os.remove(zip_path)

def make_app():
    return tornado.web.Application([
        (r"/process_video", ProcessVideoHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
