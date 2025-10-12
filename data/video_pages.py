import json

from flask import Blueprint, render_template, abort, send_from_directory, current_app

import os

video_pages = Blueprint('video_pages', __name__, template_folder='templates')

# Specify where the videos.json is located here.
videos_json_file = 'json/videos.json'

# Base directory where videos are stored
# video_directory = os.path.join(flask_web.app.root_path, 'media', 'videos')

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

    return render_template('video_template.html',
                           video_title=video_data['title'],
                           video_description=video_data['description'],
                           video_file=video_data['file'])


@video_pages.route('/media/videos/<path:filename>')
def serve_video(filename):
    # Use current_app to access the root_path
    video_directory = os.path.join(current_app.root_path, 'media', 'videos')
    video_path = os.path.join(video_directory, filename)

    # Additional check to confirm file existence
    if not os.path.isfile(video_path):
        abort(404)

    return send_from_directory(video_directory, filename)


#-----------------
# End video pages
#-----------------