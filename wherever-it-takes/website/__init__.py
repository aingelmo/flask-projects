import importlib
import os
from os import path

import dash
from flask import Flask
from flask.helpers import get_root_path

DB_NAME = "database.db"


def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_NAME}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    register_extensions(app)
    register_blueprints(app)
    register_dashapp(app)

    return app


def register_dashapp(app):
    # Find all Dash apps file (who's name ends with "_dash_app.py")
    files = [
        f
        for f in os.listdir(os.path.join(os.path.dirname(__file__), "dash_apps"))
        if f.endswith("_dash_app.py")
    ]

    # Import all Dash apps and call their create_app() function
    for file in files:
        module = importlib.import_module("website.dash_apps." + file[:-3])
        app = module.create_dash(app)


def register_extensions(app):
    from website.extensions import db, login

    db.init_app(app)
    login.login_view = "auth.login"
    login.init_app(app)

    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")


def register_blueprints(app):
    from website import auth, user, views

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.base_app)
    app.register_blueprint(user.bp)
