import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from . import app
from .database import session

'''post_schema = {
    "properties" : {
        "file" : {
            "type" : "object",
            "required" :["id"],
            "properties" : {
                "id" : {"type:" : "int"}
            }
        }
    },
    "required" :
        ["file"]
}'''

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """Get a list of posts """
#    post_like = request.args.get("title_like")

    # Get and filter the posts from the database
    posts = session.query(models.Post)
#    if title_like:
    #        posts = posts.filter(models.Post.title.contains(title_like))
    #
    #    if body_like:
    #        posts = posts.filter(models.Post.body.contains(body_like))
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