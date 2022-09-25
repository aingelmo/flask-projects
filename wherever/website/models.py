from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from website.extensions import db, login_manager


@login_manager.user_loader
def loaduser(id):
    return Users.query.get(int(id))


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    google_user_id = db.Column(db.String(64), db.ForeignKey("google_users.id"))
    google_users = db.relationship(
        "GoogleUsers", backref=db.backref("users", lazy=True)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class GoogleUsers(db.Model):
    __tablename__ = "google_users"
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    profile_pic = db.Column(db.String(256), index=True, unique=True)

    def __repr__(self) -> str:
        return f"<User {self.email}>"
