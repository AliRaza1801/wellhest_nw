import os

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DB_USER')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}/{os.getenv('DB_SCHEMA')}"

app.config['SECRET_KEY'] = 'ZDYdjgYL68NwAUPSd-rQOZVcoVc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config.update(dict(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
))

mail = Mail(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

store = HttpExposedFileSystemStore(
    path=BASE_DIR,
    prefix='media/images/'
)
