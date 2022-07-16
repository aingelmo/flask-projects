from flask import Flask

from second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="")


@app.route("/")
def test():
    return "<h1>TEST</h1>"


if __name__ == "__main__":
    app.run(debug=True)
