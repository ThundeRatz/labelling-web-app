import os

from flask import current_app

def get_download_url(file_id):
    try:
        url = current_app.config["B2_DOWNLOAD_URL"]
    except KeyError:
        raise RuntimeError("Missing B2_DOWNLOAD_URL config variable")
    return f"{url}/b2api/v1/b2_download_file_by_id?fileId={file_id}"
