import json

from flask import Blueprint, render_template, abort, send_from_directory, current_app, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import os

from models import User, bcrypt, video_auth, params_video_serve

video_pages = Blueprint('video_pages', __name__, template_folder='templates')

# Specify where the videos.json is located here.
videos_json_file = 'json/videos.json'

# Base directory where videos are stored
# video_directory = os.path.join(flask_web.app.root_path, 'media', 'videos')

# This should get the current video id from the file name, for use with going to the video when authenticated.
def get_video_id_from_filename(filename):
    with open(videos_json_file, 'r') as f:
        videos = json.load(f)

    for video_id, video in videos.items():
        if video['file'] == filename:
            return video_id

    return None

#----------------
# Video pages
#----------------

# Main Video page
@video_pages.route("/videos")

# def video_main_page():
    # return render_template("videos.html")

def video_main_page():
    # Load videos from JSON file
    try:
        with open(videos_json_file, 'r') as f:
            videos = json.load(f)
    except FileNotFoundError:
        abort(500, "Video data not found.")
    except json.JSONDecodeError:
        abort(500, "Error decoding video data.")

    return render_template('video_list.html', videos=videos)  # Make sure 'videos' is passed!

@video_pages.route('/video/<video_id>')
def video_page(video_id):
# Made this somewhat mimic the YouTube /watch?v syntax
# Gets the video_id like this: http://localhost:8081/watch?v=1
# Replaces old method which does it like this: http://localhost:8081/video/1

# @video_pages.route('/watch')
# def video_page():
#     if params_video_serve:
#         video_id = request.args.get('v')
    # if not video_id:
    #     abort(400, "Video ID is required.")

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
    video_restricted = video_data.get('restricted')
    if video_auth:
        if video_restricted and not current_user.is_authenticated:
            flash('You must be logged in to view this video.', 'danger')
            session['next'] = url_for('video_pages.video_page', video_id=video_id)  # Store video URL
            # print("Next video URL set in session:", session['next'])  # Debugging line
            # session['next'] = url_for('video_pages.video_page', v=video_id)  # Store video URL]
            # print(str(video_restricted) + " not logged in")
            return redirect(url_for('login_pages.login'))

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

    # Add video auth check here, if the video requires auth this disables direct access of the files.
    if video_auth:
        if not current_user.is_authenticated:
            return redirect(url_for('login_pages.login'))

    return send_from_directory(video_directory, filename)




#-----------------
# End video pages
#-----------------