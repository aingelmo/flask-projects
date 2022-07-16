import email
from datetime import timedelta

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column("student_id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(50))
    password = db.Column("password", db.String(50))
    email = db.Column("email", db.String(50))

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email


db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if "username" in session:
        return redirect(url_for("user"))
    else:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]

            found_username = Users.query.filter_by(username=username).first()
            
            if not found_username:
                login_data = Users(username, password, email)
                db.session.add(login_data)
                db.session.commit()

            if username == "admin" and password == "admin":
                session["admin"] = True
                session["username"] = username
                return redirect(url_for("user"))

            elif username == "andres" and password == "andres":
                session["username"] = username
                return redirect(url_for("user"))

            else:
                error = "Invalid Credentials. Please try again."
                return render_template("login.html", error=error)

        else:
            return render_template("login.html")


@app.route("/user")
def user():
    if "username" in session:
        username = session["username"]

        if "admin" in session:
            if session["admin"]:
                return render_template("user.html", user=username, admin=True)
        else:
            return render_template("user.html", user=username, admin=False)

    else:
        return redirect(url_for("login"))


@app.route("/view")
def view():
    if "admin" in session:
        if session["admin"]:
            return render_template(
                "view.html", values=Users.query.all(), admin=True, user=True
            )

    else:
        flash("Not enough rights to see it!")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You've been signed out!")
    session.pop("username")
    if "admin" in session:
        session.pop("admin")
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
