import os

class Dev_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'really-hard-to-guess'