from flask import render_template
from flask_restful import Resource, Api
import json
import dateutil.parser as dp

from . import app
from . import models
from .database import session
from . import api

@app.route("/", methods=["GET"])
def start():

    response = api.posts_get()

    posts = json.loads(response.data.decode("ascii"))

    return render_template("index.html",
                           posts=posts,
                           dp=dp.parse)

@app.route("/", methods=["POST"])
def add_label():
    response = api.post_label()

    response = json.loads(response.data.decode("ascii"))

    return render_template("index.html",
                            response)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

