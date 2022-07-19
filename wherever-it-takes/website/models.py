from flask_login import UserMixin

from . import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
