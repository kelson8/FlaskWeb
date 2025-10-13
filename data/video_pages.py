import json

from flask import Blueprint, render_template, abort, send_from_directory, current_app, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import os

from models import User, users

video_pages = Blueprint('video_pages', __name__, template_folder='templates')

# Specify where the videos.json is located here.
videos_json_file = 'json/videos.json'

# Base directory where videos are stored
# video_directory = os.path.join(flask_web.app.root_path, 'media', 'videos')

##### Auth test
## TODO Refactor this!! It is in models.py and flask_web.py, make this use SQLite and password salting/hashing
# This is currently very insecure so it is disabled.
# login_manager = LoginManager()

# If this is true, videos with the 'restricted' value set to true in the JSON will require login.
video_auth = False

#####

#----------------
# Video pages
#----------------

# Main Video page
# TODO Setup to need auth to browse certain files.
@video_pages.route("/videos")
def video_main_page():
    return render_template("videos.html")

@video_pages.route('/video/<video_id>')
def video_page(video_id):
    # Load videos from JSON file
    try:
        with open(videos_json_file, 'r') as f:
            videos = json.load(f)
    except FileNotFoundError:
        abort(500, "Video data not found.")
    except json.JSONDecodeError:
        abort(500, "Error decoding video data.")

    video_data = videos.get(video_id)

    if not video_data:
        abort(404)

    # This was just for testing
    # print(f"Restricted: {video_data.get('restricted')}, Authenticated: {current_user.is_authenticated}")

    # Adds auth for videos here
    # TODO Fix this to use hashed and salted passwords in a SQLite file.
    video_restricted = video_data.get('restricted')
    if video_auth:

        if video_restricted and not current_user.is_authenticated:
            # print(str(video_restricted) + " not logged in")
            return redirect(url_for('video_pages.login'))

    return render_template('video_template.html',
                           video_title=video_data['title'],
                           video_description=video_data['description'],
                           video_file=video_data['file'],
                           video_is_restricted=video_restricted)

@video_pages.route('/media/videos/<path:filename>')
# @login_required
def serve_video(filename):
    # Use current_app to access the root_path
    video_directory = os.path.join(current_app.root_path, 'media', 'videos')
    video_path = os.path.join(video_directory, filename)

    # Additional check to confirm file existence
    if not os.path.isfile(video_path):
        abort(404)

    return send_from_directory(video_directory, filename)

#### Auth Test
# I got this working, this needs to have logins implemented in SQLite and with password salting/hashing
# @video_pages.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users and users[username] == password:
#             user = User(username)
#             login_user(user)
#             return redirect(url_for('video_pages.video_main_page'))
#         flash('Invalid username or password.')
#     return render_template('login.html')
#
# @video_pages.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('video_pages.login'))

####


#-----------------
# End video pages
#-----------------