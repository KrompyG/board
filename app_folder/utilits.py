import os
from app_folder import app

# checking file's extension
def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'])

# forming photo_path for passing it into template
def form_photo_path(photoname):
    return os.path.join('\\static', 'img', 'products', photoname)
