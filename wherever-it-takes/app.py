from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "hello"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        return redirect(url_for("user"))

    else:
        return render_template("login.html")


@app.route("/user")
def user():
    return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True)
