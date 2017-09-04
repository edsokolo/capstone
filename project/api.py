import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from . import app
from .database import session


@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """Get a list of posts """
    post_like = (request.args.get("search"))
    try:
        date_start = request.args.get("date_start")
        date_start = date_start.strftime('%Y-%m-%d')
    except: AttributeError

    try:
        date_end = request.args.get("date_end")
        date_end = date_end.strftime('%Y-%m-%d')
    except: AttributeError

    # Get and filter the posts from the database
    posts = session.query(models.Post)
    if post_like:
        post_like = post_like.lower()
        posts = posts.filter(models.Post.content.contains(post_like))

    if date_start:
        posts = posts.filter(models.Post.created_time >= date_start)

    if date_end:
        posts = posts.filter(models.Post.created_time <= date_end)

    posts = posts.order_by(models.Post.created_time)


    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/label/association_add", methods=["GET","POST"])
@decorators.accept("application/json")
def post_label():
    label_name = request.form["label"]
    post_id = request.form["hidden"]

    post = session.query(models.Post).filter(models.Post.id == post_id).all()

#    if title_like:
    #        posts = posts.filter(models.Post.title.contains(title_like))
    #
    #    if body_like:
    #        posts = posts.filter(models.Post.body.contains(body_like))

    label = session.query(models.Label).filter(models.Label.name == label_name).all()
    label = label[0]

    ##Add logic that flashs
    if not label:
        message = "Could not find label {}".format(label_name)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    post[0].labels.append(label)

    session.add(label)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(label.as_dictionary())
    headers = {"Location": url_for("start", id=label.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")


@app.route("/api/label/association_delete", methods=["POST"])
@decorators.accept("application/json")
def delete_label():
    post_id = request.form["hidden1"]
    label_id = request.form["delete"]

    posts = session.query(models.Post).filter(models.Post.id == post_id).all()
    post = posts[0]

    labels = session.query(models.Label).filter(models.Label.id == label_id).all()
    label = labels[0]

    labels = post.labels
    labels.remove(label)


    if not label:
        message = "Could not find association with post_id {} and label_id {}".format(post_id, label_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    message = "Association with post_id {} and label_id {} is deleted".format(post_id, label_id)
    data = json.dumps({"message": message})
    return Response(data, 201, mimetype="application/json")

@app.route("/api/labels", methods=["GET"])
@decorators.accept("application/json")
def labels_get():
    """Get a list of posts """
    label_like = (request.args.get("search"))
    try:
        date_start = request.args.get("date_start")
        date_start = date_start.strftime('%Y-%m-%d')
    except: AttributeError

    try:
        date_end = request.args.get("date_end")
        date_end = date_end.strftime('%Y-%m-%d')
    except: AttributeError

    # Get and filter the posts from the database
    labels = session.query(models.Label)

    if label_like:
        label_like = label_like.lower()
        labels = labels.filter(models.Label.name.contains(label_like))

    if date_start:
        labels = labels.filter(models.Label.created_time >= date_start)

    if date_end:
        labels = labels.filter(models.Label.created_time <= date_end)

    labels = labels.order_by(models.Label.created_time.desc())


    # Convert the posts to JSON and return a response
    data = json.dumps([label.as_dictionary() for label in labels])
    return Response(data, 200, mimetype="application/json")

@app.route("/api/label/delete", methods=["POST"])
@decorators.accept("application/json")
def api_drop_label():
    label_id = request.form["label_id"]

    labels = session.query(models.Label).filter(models.Label.id == label_id).all()
    label = labels[0]

    if not label:
        message = "Could not find association with label {}".format(label.name)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    session.delete(label)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    message = "Label {} is deleted".format(label.name)
    data = json.dumps({"message": message})
    return Response(data, 201, mimetype="application/json")

@app.route("/api/label/add", methods=["GET","POST"])
@decorators.accept("application/json")
def api_new_label():
    label_name = request.form["label_name"]

    if len(label_name) == 0:
        message = "Blank labels not allowed"
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    label = models.Label(name=label_name)

    session.add(label)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    message = "Label {} is created".format(label_name)
    data = json.dumps({"message": message})
    return Response(data, 201, mimetype="application/json")