import db.access as db
from flask import Flask, jsonify, redirect, render_template, request
import storage.b2 as b2

app = Flask(__name__)


@app.route('/label')
def label_page():
    image_id = db.get_one_pending()
    if not image_id:
        return redirect('static/no_more_images.html')
    image_link = b2.get_download_url(image_id)
    return render_template('label.html', image_link=image_link, image_id=image_id)


@app.route('/post_label', methods=['POST'])
def label_post():
    payload = request.get_json()
    db.set_label(payload['image_id'], payload['labels'])
    return jsonify(status='OK')
