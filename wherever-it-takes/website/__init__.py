from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev", SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_NAME}"
    )
    db.init_app(app)

    from .auth import bp

    app.register_blueprint(bp)

    from .models import Users

    create_database(app)

    @app.route("/hello")
    def hello():
        return "Hello World"

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
