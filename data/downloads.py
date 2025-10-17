from flask import Blueprint, render_template, jsonify, request, abort, send_from_directory, send_file, url_for
import os
import requests

import logging
from config import Config

from flask_login import current_user

downloads = Blueprint('downloads', __name__, template_folder='templates')

# https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html

# This seems to work fine for docker, I don't think the other one is needed
# upload_directory = "./downloads/"
# upload_directory = "/downloads/"

# New for docker volume, SWITCH BACK!!!
# upload_directory = "/mnt/docker_volume/flask_downloads"

# For local testing
# if Config.docker_enabled:
if Config.is_docker_enabled:
    upload_directory = "/downloads/"
else:
    upload_directory = Config.download_directory

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
# @downloads.route("/download/<path:sub_path>")
def list_files():
# def list_files(sub_path=""):
    """ List files on the server. -- Enabled for logged in users only """

    if current_user.is_authenticated:
        files = os.listdir(upload_directory)
        # Create full URLs for each file if necessary
        file_urls = [url_for('downloads.get_file', path=file) for file in files]
        return render_template("file_listing.html", files=file_urls)

    # TODO Fix this to work, it should traverse the other directories if logged in, and display subfolder contents.
    # if current_user.is_authenticated:
    #     full_path = os.path.join(upload_directory, sub_path)
    #
    #     file_urls = []
    #
    #     for root, dirs, files in os.walk(full_path):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             rel_path = os.path.relpath(file_path, upload_directory)
    #             file_urls.append(('downloads.get_file', file_path))
    #     return render_template("file_listing.html", file_urls=file_urls)
    else:
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
