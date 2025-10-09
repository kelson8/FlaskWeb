from flask import Blueprint, render_template, jsonify, request, abort, send_from_directory, send_file
import os
import requests


import logging

about_pages = Blueprint('about_pages', __name__, template_folder='templates')

#-----------------
# About pages
#-----------------

@about_pages.route("/about")
def about_main_page():
    return render_template("/about/about.html")

# Fivem Server
@about_pages.route("/about-fivem")
def about_fivem_page():
    return render_template("/about/about-fivem.html")

# Minecraft Server
@about_pages.route("/about-mc")
def about_mc_page():
    return render_template("/about/about-mc.html")

# I haven't set these two up yet.
# Minecraft server image page
# @about_pages.route("/mc-photos")
# def mc_photos_page():
#     return render_template("mc-photos.html")
#

# I need to get the gitea server working for this one, most links are internal only so I'll leave it for later
# @about_pages.route("/about-code")
# def about_code_page():
    # return render_template("about-code.html")