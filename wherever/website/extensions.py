from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from oauthlib.oauth2 import WebApplicationClient
from settings import GOOGLE_CLIENT_ID

db = SQLAlchemy()
login = LoginManager()
client = WebApplicationClient(GOOGLE_CLIENT_ID)
