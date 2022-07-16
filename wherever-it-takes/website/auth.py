from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Users

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.user"))
            else:
                flash("Incorrect password", category="error")

        else:
            flash("Email does not exists", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", category="success")
    return redirect(url_for("auth.login"))


@auth.route("sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = Users.query.filter_by(email=email).first()

        if user:
            flash("User already registered", category="error")
        elif len(email) < 5:
            flash("Email must be at least 4 characters long", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 4 characters long", category="error")
        elif password1 != password2:
            flash("Passwords do not match. Try again.", category="error")
        else:
            new_user = Users(
                email=email, password=generate_password_hash(password1, method="sha256")
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("Account created", category="success")

            return redirect(url_for("views.user"))

    return render_template("sign-up.html", user=current_user)
