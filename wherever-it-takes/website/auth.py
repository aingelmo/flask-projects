from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Users

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        error = None

        user = Users.query.filter_by(username=username).first()

        if user:
            error = "There is already an user registered with that name."
        elif len(username) < 4:
            error = "Select a username with at least 3 characters."
        elif len(email) < 10:
            error = "Type an email with at least 10 characters."
        elif len(password) < 4:
            error = "The password must contain at least 4 characters."
        elif password != password_confirmation:
            error = "Passwords do not match."

        if error is None:
            new_user = Users(
                username=username,
                email=email,
                password=generate_password_hash(password),
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Account successfully created!", category="success")

        else:
            flash(error, category="error")

    return render_template("auth/register.html")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        print(username)

        error = None

        if user is None:
            error = "Username does not exist."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password. Please, try again."

        if error is None:
            login_user(user, remember=True)
            flash("Logged in successfully!", category="success")
            return redirect(url_for("auth.register"))

        else:
            flash(error, category="error")

    return render_template("auth/login.html")


@bp.route("logout")
def logout():
    logout_user
    flash("Logged out successfully!", category="success")
    return redirect(url_for("auth.login"))
