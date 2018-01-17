from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)
db = MongoEngine(app)
login = LoginManager(app)
login.login_view = 'login'
# app.session_interface = MongoEngineSessionInterface(db)
migrate = Migrate(app, db)

from app import routes, models
