from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from . import auth, models, user, views

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_NAME}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    models.db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(user.bp)

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.Users.query.get(int(id))

    @app.route("/hello")
    def hello():
        return "Hello World"

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        models.db.create_all(app=app)
        print("Created Database!")
