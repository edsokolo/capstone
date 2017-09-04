from flask import render_template
from flask_restful import Resource, Api
import json
import dateutil.parser as dp
import datetime as dt


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
                           dp=dp.parse,
                           dt=dt)

@app.route("/", methods=["POST"])
def add_label():
    label_response = api.post_label()
    label_data = json.loads(label_response.data.decode("ascii"))

    post_response = api.posts_get()
    posts = json.loads(post_response.data.decode("ascii"))

    return render_template("index.html",
                           data=label_data,
                           posts=posts,
                           dp=dp.parse,
                           dt=dt)

@app.route("/remove", methods=["POST"])
def remove_label():
    label_response = api.delete_label()
    label_data = json.loads(label_response.data.decode("ascii"))

    post_response = api.posts_get()
    posts = json.loads(post_response.data.decode("ascii"))

    return render_template("index.html",
                           data=label_data,
                           posts=posts,
                           dp=dp.parse,
                           dt=dt)


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/labels", methods=["GET"])
def start_continue():
    response = api.labels_get()
    labels = json.loads(response.data.decode("ascii"))

    return render_template("labels.html",
                           labels=labels,
                           dp=dp.parse,
                           dt=dt)

@app.route("/labels", methods=["POST"])
def drop_label():
    drop_response = api.api_drop_label()
    dropped_label = json.loads(drop_response.data.decode("ascii"))

    get_response = api.labels_get()
    labels = json.loads(get_response.data.decode("ascii"))

    return render_template("labels.html",
                           dropped=dropped_label,
                           labels=labels,
                           dp=dp.parse,
                           dt=dt)

@app.route("/label_added", methods=["GET","POST"])
def new_label():
    add_response = api.api_new_label()
    added_label = json.loads(add_response.data.decode("ascii"))

    get_response = api.labels_get()
    labels = json.loads(get_response.data.decode("ascii"))

    return render_template("labels.html",
                           added=added_label,
                           labels=labels,
                           dp=dp.parse,
                           dt=dt)