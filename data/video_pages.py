from flask import Blueprint, render_template, abort

video_pages = Blueprint('video_pages', __name__, template_folder='templates')


#-----------------
# Video pages
#-----------------

# Main Video page
# TODO Setup to need auth to browse certain files.
@video_pages.route("/videos")
def video_main_page():
    return render_template("videos.html")

# To add new video pages, add the file in
@video_pages.route('/video/<video_id>')
def video_page(video_id):
    # Example data fetch for demonstration purposes
    videos = {
        '1': {
            'title': "Tom Clancy's Ghost Recon Wildlands Chopper glitch",
            'description': "I'm not sure how I would do this again, it just randomly happened one day.",
            'file': 'videos/tom_clancy_wildlands_glitch1.mp4'
        },
        '2': {
            'title': "ReVC Spinning Cars",
            'description': "I coded this function using C++ to mess around with, the game crashes at the end.",
            'file': 'videos/ReVC-SpinningCars.mp4'
        },
        '3': {
            'title': "ReVC KCNet ImGui Test",
            'description': "This is a ImGui mod menu I am working on in C++ using ReVC.",
            'file': 'videos/ReVC-KCNet-ImGuiMenu1.mp4'
        }
    }

    video_data = videos.get(video_id)

    if not video_data:
        abort(404)

    return render_template('video_template.html',
                           video_title=video_data['title'],
                           video_description=video_data['description'],
                           video_file=video_data['file'])


# Tom clancy ghost recon wildlands glitches
# Glitch #1 (Chopper flies into the air after land)
# @video_pages.route("/video1")
# def video1_page():
#     return render_template("video1.html")


# # ReVC Spinning cars
# @video_pages.route("/video2")
# def video2_page():
#     return render_template("video2.html")


#-----------------
# End video pages
#-----------------