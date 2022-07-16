from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/user")
@login_required
def user():
    return render_template("user.html", user=current_user)
