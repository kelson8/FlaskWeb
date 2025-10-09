from flask import Blueprint, render_template, jsonify, request, abort, send_from_directory, send_file
import os
import requests


import logging

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
    return render_template("errors/file-error.html")


@downloads.route("/download/<path:path>")
def get_file(path):
    """ Download a file. """
    return send_from_directory(upload_directory, path, as_attachment=True)

#-----------------
# Display custom files in browser
#-----------------

### Disabled, I think this is causing a crash?
# Display .sh files in browser instead of just downloading them.
# @downloads.route('/download/scripts/<path:filename>')
# def serve_script(filename):
#     # Moved import here, otherwise it breaks.
#     from flask_web import logEnabled, logger
#     # Define the directory where .sh files are stored
#     # Local desktop test
#     scripts_dir = '/downloads/scripts/'
#
#     # Construct the full path to the script file
#     file_path = os.path.join(scripts_dir, filename)
#
#     # Check if the file exists
#     if os.path.isfile(file_path):
#         # Log the IP address accessing the file
#         client_ip = request.remote_addr
#         if logEnabled:
#             logging.info(f"Access attempt: {client_ip} requested {file_path}")
#
#         return send_file(file_path, mimetype='text/plain', as_attachment=False)
#     else:
#         # Log an error message and return a 404 if the file does not exist
#         # app.logger.error(f"File not found: {file_path}")
#         if logEnabled:
#             logger.error('%s is not a file', filename)
#         # print(f"Trying to serve file: {file_path}")
#         # return send_file(file_path, mimetype='text/plain')
# ##
