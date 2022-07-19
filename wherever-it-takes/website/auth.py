from flask import Blueprint, flash, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Users

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        error = None

        if len(user) < 4:
            error = "Select a username with at least 3 characters."
        elif len(email) < 10:
            error = "Type an email with at least 10 characters."
        elif len(password) < 4:
            error = "The password must contain at least 4 characters."
        elif password != password_confirmation:
            error = "Passwords do not match."

        if error is None:
            new_user = Users(
                user=user, email=email, password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            
        flash(error)
        
    return render_template("auth/register.html")


@auth.route("/login")
def login():
    pass
