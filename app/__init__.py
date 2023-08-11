from flask import Flask
from app.db import init_app
from config import Config
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(Config)
init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from app import routes


