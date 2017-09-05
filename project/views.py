from flask import render_template, request, redirect, url_for, flash
from flask_restful import Resource, Api
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash


import json
import dateutil.parser as dp
import datetime as dt


from . import app
from . import models
from .database import session
from . import api

@app.route("/", methods=["GET"])
def start():
    logged_in = current_user.is_authenticated
    response = api.posts_get()
    posts = json.loads(response.data.decode("ascii"))

    return render_template("index.html",
                           posts=posts,
                           logged_in=logged_in,
                           dp=dp.parse,
                           dt=dt)

@app.route("/", methods=["POST"])
@login_required
def add_label():
    logged_in = current_user.is_authenticated
    label_response = api.post_label()
    label_data = json.loads(label_response.data.decode("ascii"))

    post_response = api.posts_get()
    posts = json.loads(post_response.data.decode("ascii"))

    return render_template("index.html",
                           data=label_data,
                           posts=posts,
                           logged_in=logged_in,
                           dp=dp.parse,
                           dt=dt)

@app.route("/remove", methods=["POST"])
@login_required
def remove_label():
    logged_in = current_user.is_authenticated
    label_response = api.delete_label()
    label_data = json.loads(label_response.data.decode("ascii"))

    post_response = api.posts_get()
    posts = json.loads(post_response.data.decode("ascii"))

    return render_template("index.html",
                           data=label_data,
                           posts=posts,
                           logged_in=logged_in,
                           dp=dp.parse,
                           dt=dt)

@app.route("/login", methods=["GET"])
def login_get():
    logged_in = current_user.is_authenticated
    return render_template("login.html",
                               logged_in=logged_in,)

@app.route("/login", methods=["POST"])
def login_post():
    logged_in = current_user.is_authenticated
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(models.User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    logged_in = current_user.is_authenticated
    return redirect(request.args.get('previous') or request.args.get('next') or url_for("start"))

@app.route("/logout", methods=["GET"])
def logout_get():
    logout_user()
    logged_in = current_user.is_authenticated
    return redirect(request.referrer)


@app.route("/labels", methods=["GET"])

def start_continue():
    logged_in = current_user.is_authenticated
    response = api.labels_get()
    labels = json.loads(response.data.decode("ascii"))

    return render_template("labels.html",
                           labels=labels,
                           dp=dp.parse,
                           logged_in=logged_in,
                           dt=dt)

@app.route("/labels", methods=["POST"])
@login_required
def drop_label():
    logged_in = current_user.is_authenticated
    drop_response = api.api_drop_label()
    dropped_label = json.loads(drop_response.data.decode("ascii"))

    get_response = api.labels_get()
    labels = json.loads(get_response.data.decode("ascii"))

    return render_template("labels.html",
                           dropped=dropped_label,
                           labels=labels,
                           logged_in=logged_in,
                           dp=dp.parse,
                           dt=dt)

@app.route("/label_added", methods=["GET","POST"])
@login_required
def new_label():
    logged_in = current_user.is_authenticated
    add_response = api.api_new_label()
    added_label = json.loads(add_response.data.decode("ascii"))

    get_response = api.labels_get()
    labels = json.loads(get_response.data.decode("ascii"))

    return render_template("labels.html",
                           added=added_label,
                           labels=labels,
                           logged_in=logged_in,
                           dp=dp.parse,
                           dt=dt)