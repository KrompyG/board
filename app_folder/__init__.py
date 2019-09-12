from flask import Flask
from config import Dev_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Dev_config)
db = SQLAlchemy(app)
migrate = Migrate(db, app)

from app_folder import routes, models
