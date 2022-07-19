import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev", SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_NAME}"
    )
