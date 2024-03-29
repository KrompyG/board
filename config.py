import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Dev_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'really-hard-to-guess'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASEDIR = basedir
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    STATIC_FOLDER = os.path.join(BASEDIR, 'app_folder', 'static')
    # if you want to change product photo folder
    # you have to change
    # 0) PRODUCT_PHOTO_FOLDER
    # 1) form_photo_path(photoname) function (utilits.py)
    PRODUCT_PHOTO_FOLDER = os.path.join(STATIC_FOLDER, 'img', 'products')
    APP_ID = '7174211'
    PROTECTED_KEY = 'LULoGsnEBXDPpOhr7kIR'
    OFFER_STATUS = 1
    REQUEST_STATUS = 2
