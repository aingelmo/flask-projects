from os import path

import dash
from flask import Flask
from flask.helpers import get_root_path

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_NAME}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from website.dash_app.callbacks import register_callbacks
    from website.dash_app.layout import layout

    register_dashapp(app, "Dashapp 1", "dashboard", layout, register_callbacks)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }

    my_dashapp = dash.Dash(
        __name__,
        server=app,
        url_base_pathname=f"/{base_pathname}/",
        assets_folder=get_root_path(__name__) + f"/{base_pathname}/assets/",
        meta_tags=[meta_viewport],
    )

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)


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
    app.register_blueprint(views.bp)
    app.register_blueprint(user.bp)
