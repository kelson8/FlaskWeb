from flask import Blueprint, render_template

video_pages = Blueprint('video_pages', __name__, template_folder='templates')


#-----------------
# Video pages
#-----------------

# Main Video page
# TODO Setup to need auth to browse certain files.
@video_pages.route("/videos")
def video_main_page():
    return render_template("videos.html")

# Tom clancy ghost recon wildlands glitches
# Glitch #1 (Chopper flies into the air after land)
@video_pages.route("/video1")
def video1_page():
    return render_template("video1.html")


# ReVC Spinning cars
@video_pages.route("/video2")
def video2_page():
    return render_template("video2.html")


#-----------------
# End video pages
#-----------------