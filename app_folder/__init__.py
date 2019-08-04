from flask import Flask
from config import Dev_config

app = Flask(__name__)
app.config.from_object(Dev_config)

from app_folder import routes