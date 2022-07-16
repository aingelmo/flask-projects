from flask_login import UserMixin

from . import db


class Users(db.Model, UserMixin):
    id = db.Column("student_id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(50))
    password = db.Column("password", db.String(50))
