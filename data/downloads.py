from flask import Blueprint, render_template, jsonify, request, abort, send_from_directory
import os
import requests

downloads = Blueprint('downloads', __name__, template_folder='templates')

# https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html

# This seems to work fine for docker, I don't think the other one is needed
# upload_directory = "./downloads/"
upload_directory = "/downloads/"

# New for docker volume, SWITCH BACK!!!
# upload_directory = "/mnt/docker_volume/flask_downloads"

# Not tested.
upload_directory_docker = "/app/downloads"

if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)

# @downloads.route("/download")
# def list_files():
#     """ List files on the server. """
#     files = []
#     for file_name in os.listdir(upload_directory):
#         path = os.path.join(upload_directory, file_name)
#         if os.path.isfile(path):
#             files.append(file_name)
#     return jsonify(files)

@downloads.route("/download")
def list_files():
    """ List files on the server. -- Disabled """
    return render_template("file-error.html")


@downloads.route("/download/<path:path>")
def get_file(path):
    """ Download a file. """
    return send_from_directory(upload_directory, path, as_attachment=True)
