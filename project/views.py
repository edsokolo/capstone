from flask import render_template

from . import app
from . import models
from .database import session

@app.route("/", methods=["GET"])
def start():
    return render_template("index.html")
