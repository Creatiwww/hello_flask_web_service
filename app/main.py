from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
import database as db

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/initdb")
def initdb():
    return db.init_db()


@app.route("/getall")
def get_all():
    return db.get_all()


@app.route("/add/<username>")
def add(username):
    return db.add(user_name=username)


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
