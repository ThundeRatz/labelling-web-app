from flask import Flask, jsonify, redirect, render_template, request

import db.access as db
import storage.b2 as b2
import sys

app = Flask(__name__)

try:
    app.config.from_pyfile("config2.py")
except FileNotFoundError:
    raise RuntimeError('Config file config.py not found on root folder!')


@app.route("/")
def label_page():
    image_id = db.get_one_pending()
    if not image_id:
        return render_template("no_more_images.html")
    image_link = b2.get_download_url(image_id)
    return render_template("label.html", image_link=image_link, image_id=image_id)


@app.route("/tutorial")
def tutorial_page():
    return render_template("tutorial.html")


@app.route("/post_label", methods=["POST"])
def label_post():
    payload = request.get_json()
    db.set_label(payload["image_id"], payload["labels"])
    return jsonify(status="OK")
