# Logger
import logging
# Time for logging
from time import strftime

from flask import Flask, url_for, request, render_template, jsonify, redirect, make_response
from flask_cors import CORS, cross_origin

import os
from os.path import join, dirname
from dotenv import load_dotenv

from test_pages import simple_page
from password_gen import password_gen

###
# Downloads page
from downloads import downloads
# Form test page
#from form_test import form_test

# TODO Look into this later: https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript

# Disable the password generator for now.
passwordGenEnabled = False

# Setup .env file for database password
# https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Set up the app, and login manager
app = Flask(__name__)

# https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Split the app into multiple python files
# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files
app.register_blueprint(simple_page)
# Downloads page
app.register_blueprint(downloads)
# Form test page
#app.register_blueprint(form_test)

app.secret_key= os.environ.get("SECRET_KEY")

# Setup logging
# https://github.com/google/openhtf/issues/46
# https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module

### New for traefik, shows real IPs

# Basic class to get the HTTP_CF_CONNECTING_IP, or HTTP_X_FORWARDED_FOR headers.
class CloudflareProxyFix:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Cloudflare sets CF-Connecting-IP
        if 'HTTP_CF_CONNECTING_IP' in environ:
            environ['REMOTE_ADDR'] = environ['HTTP_CF_CONNECTING_IP']
        # Fallback to X-Forwarded-For if CF-Connecting-IP is not present,
        # but only take the first IP (the real client IP).
        elif 'HTTP_X_FORWARDED_FOR' in environ:
            # X-Forwarded-For can contain multiple IPs (client, proxy1, proxy2)
            # We want the leftmost one (the client)
            forwarded_for_ips = environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
            environ['REMOTE_ADDR'] = forwarded_for_ips
        return self.app(environ, start_response)

# Apply the custom middleware
app.wsgi_app = CloudflareProxyFix(app.wsgi_app)

###
#-----------------
# This toggles the logging to file on and off, useful for debugging without writing to the logs.
#-----------------
logEnabled = True
if logEnabled:
    log_file = "flask.log"
    logging.basicConfig(filename=log_file, filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

#-----------------
# Add favicon route
#-----------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#-----------------
# Logging
#-----------------

# https://stackoverflow.com/questions/52372187/logging-with-command-line-waitress-serve
# https://flask.palletsprojects.com/en/2.3.x/logging/
# Test
# This seems to log everything with errors

#-----------------
# Disable this for local network for testing.
#-----------------
if logEnabled:
    @app.after_request
    def after_request(response):
        # TODO Why does this get the incorrect time on the VPS? Try to fix that.
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        # https://stackoverflow.com/questions/15670763/strftime-gets-wrong-date
        # timestamp = strftime('[%a, %d %b %Y %I:%M:%S %p %Z]')

        # This gets the response without the message, strips the 'OK' or other messages
        string_response = str.split(response.status)[0]

        # Ok or not modified
        # if response.status == 200 or response.status == 304:
        if string_response == "200" or string_response == "304":
            # print("Hello")
            logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
                        request.full_path, response.status)
        else:
            logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
                         request.full_path, response.status)
            # print(string_response)
            # print(str.split(response.status)[0])

        # else:
        #     logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
        return response

#-----------------



#-----------------
# Pages
#-----------------

@app.route("/")
def index():
    # client_ip = request.remote_addr
    # logging.info(f"Request from IP: {client_ip}")
    return render_template("index.html")
    # return render_template("index.html", password=password_gen(20))

if passwordGenEnabled:
    @app.route("/passwordgen")
    def password_gen_test():
        return password_gen(20)

#-----------------
# Error pages
#-----------------
@app.errorhandler(404)

# 404 not found
def not_found(error):
    return render_template("errors/404.html")

# 403 access denied
@app.errorhandler(403)
def access_denied(error):
    return render_template("errors/403.html")


#-----------------
# About pages
#-----------------

@app.route("/about")
def about_main_page():
    return render_template("about.html")

# Fivem Server
@app.route("/about-fivem")
def about_fivem_page():
    return render_template("about-fivem.html")

# Minecraft Server
@app.route("/about-mc")
def about_mc_page():
    return render_template("about-mc.html")

# I haven't set these two up yet.
# Minecraft server image page
# @app.route("/mc-photos")
# def mc_photos_page():
#     return render_template("mc-photos.html")
#

# I need to get the gitea server working for this one, most links are internal only so I'll leave it for later
# @app.route("/about-code")
# def about_code_page():
    # return render_template("about-code.html")

@app.route("/wiki")
def wiki_page():
    return redirect("https://wiki.kelsoncraft.net/", code=302)
    # return render_template("about-mc.html")

# Forum test, enable domain when ready to make public.
# Todo Setup this forum later.
# @app.route("/forum")
# def forum_page():
#     return redirect("https://forum.kelsoncraft.net/")


#-----------------
# End about pages
#-----------------

#-----------------
# Video pages
#-----------------

# Main Video page
# TODO Setup to need auth to browse certain files.
@app.route("/videos")
def video_main_page():
    return render_template("videos.html")

# Tom clancy ghost recon wildlands glitches
# Glitch #1 (Chopper flies into the air after land)
@app.route("/video1")
def video1_page():
    return render_template("video1.html")


# ReVC Spinning cars
@app.route("/video2")
def video2_page():
    return render_template("video2.html")


#-----------------
# End video pages
#-----------------

#-----------------
# Begin Game/ReVC pages
#-----------------

@app.route("/projects")
def projects_page():
    return render_template("projects.html")

# @app.route("/revc-additions")
@app.route("/projects/revc")
# def revc_additions_page():
def revc_projects_page():
    return render_template("revc-additions.html")


#-----------------
# End Game/ReVC pages
#-----------------

if passwordGenEnabled:
    @app.route("/password_gen")
    def password_gen_page():
        return render_template("password_gen.html", passwords=password_gen(20))

#-----------------
# Test pages
#-----------------
# This one isn't ready to be published yet
# @app.route("/fivem_test")
# @cross_origin()
# def fivem_test_page():
#     return render_template("fivem-test.html")

#-----------------
# End test pages
#-----------------

# This now is supposed to be run with waitress installed like this:
# waitress-serve --port 81 flask_web:app
# I enabled app.run again for testing.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
