from flask import Flask, request


class InvalidVideoFile(Exception):
    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NoVideoFileSelected(Exception):
    status_code = 400

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class VideoUploader:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/upload_video', view_func=self.upload_video, methods=['POST'])
        self.allowed_extensions = ['mp4', 'flv']
        self.uploaded_file = None
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def upload_video(self):
        try:
            if 'video' not in request.files:
                raise NoVideoFileSelected('No video file found...')
            
            video = request.files['video']
            if video.filename == '':
                raise NoVideoFileSelected('No video file selected...')
            
            if video and self.allowed_file(video.filename):
                video.save('input_videos/' + video.filename)
                self.uploaded_file = 'input_videos/' + video.filename
                return 'File uploaded successfully', 200
            
            raise InvalidVideoFile('Invalid file type...')
        except InvalidVideoFile as e:
            return e.message, e.status_code
        except NoVideoFileSelected as e:
            return e.message, e.status_code
    
    def run(self):
        self.app.run(debug=True, port=5002, use_reloader=False)