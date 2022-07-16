from datetime import timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
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

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


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

            login_data = Users(username, password)
            db.session.add(login_data)
            db.session.commit()

            if username != "admin" or password != "admin":
                error = "Invalid Credentials. Please try again."
                return render_template("login.html", error=error)
            else:
                session["username"] = username
                return redirect(url_for("user"))

        else:
            return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You've been signed out!")
    session.pop("username")
    return redirect(url_for("login"))


@app.route("/user")
def user():
    if "username" in session:
        username = session["username"]
        return render_template("user.html", user=username, admin=True)

    else:
        return redirect(url_for("login"))


@app.route("/view")
def view():
    if "username" in session:
        return render_template("view.html", values=Users.query.all(), admin=True)

    else:
        flash("Not enough rights to see it!")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
