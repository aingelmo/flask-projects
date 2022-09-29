from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from website.extensions import db, login_manager


@login_manager.user_loader
def loaduser(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(256), unique=True)
    password_hash = db.Column(db.String(128), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class OAuth(db.Model, OAuthConsumerMixin):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(User)
