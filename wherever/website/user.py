from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/")
@login_required
def user():
    return render_template("user/user.html")
