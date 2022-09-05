from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from website.forms import LoginForm, RegistrationForm
from website.models import Users, db
from website.views import get_top_menu_items

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("views.index"))

    return render_template(
        "auth/register.html", form=form, top_menu_items=get_top_menu_items("/")
    )


@bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = "Invalid username or password"

        login_user(user, remember=form.remember_me.data)

    return render_template(
        "auth/login.html", form=form, top_menu_items=get_top_menu_items("/")
    )


@bp.route("logout")
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for("views.index"))
