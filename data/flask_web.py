# Logger
import datetime
import logging
# Time for logging
from time import strftime

import requests
from flask import Flask, url_for, request, render_template, jsonify, redirect, make_response, send_file, \
    send_from_directory, Response, abort
from flask_cors import CORS, cross_origin

## Auth test
from flask_login import LoginManager, UserMixin
from models import User, log_enabled, password_gen_enabled

import os
from os.path import join, dirname
from dotenv import load_dotenv


from password_gen import password_gen
# Pages
from test_pages import test_pages
from about_pages import about_pages
from video_pages import video_pages
from project_pages import project_pages
from misc_pages import misc_pages

###
# Downloads page
from downloads import downloads
# Form test page
#from form_test import form_test
##

from waitress import serve

import logging
from logging.handlers import TimedRotatingFileHandler

# TODO Look into this later: https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript



# Setup .env file for database password
# https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Set up the app, and login manager
app = Flask(__name__)

## New for SQLite username/password DB.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
##

# https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###
# Split the app into multiple python files
# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files
app.register_blueprint(test_pages)
# Downloads page
app.register_blueprint(downloads)
# Form test page
#app.register_blueprint(form_test)

# About pages
app.register_blueprint(about_pages)

# Video pages
app.register_blueprint(video_pages)
# Projects pages
app.register_blueprint(project_pages)

# Misc pages
app.register_blueprint(misc_pages)
###

app.secret_key = os.environ.get("SECRET_KEY")

# Setup logging
# https://github.com/google/openhtf/issues/46
# https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module

#### Auth test
# TODO Fix this to use SQLite
login_manager = LoginManager()
login_manager.login_view = 'video_pages.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

####

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
# New loading pages test
#-----------------

def register_blueprints():
    # Split the app into multiple python files
    # https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files
    app.register_blueprint(test_pages)
    # Downloads page
    app.register_blueprint(downloads)
    # Form test page
    # app.register_blueprint(form_test)

    # About pages
    app.register_blueprint(about_pages)

    # Video pages
    app.register_blueprint(video_pages)
    # Projects pages
    app.register_blueprint(project_pages)
    ###

# TODO Figure out how to use this with WGSI or Waitress Server for VPS.
def setup_app():
    register_blueprints()

#-----------------
# This toggles the logging to file on and off, useful for debugging without writing to the logs.
# TODO Test new log format, this should rotate the logs and remove old ones.
#-----------------

if log_enabled:
    # Create a handler that rotates logs at midnight

    # TODO Test this new setup in Docker, I moved the log file to logs/flask.log
    # Altough this seems to get the folder from the root of this where requirements.txt is, it may be broken on docker.
    # if not os.path.exists(os.path.join(os.getcwd() + "/" + "logs" + "/")):
    #     print("Log directory doesn't exist, creating it for you.")
    #     os.mkdir(os.path.join(os.getcwd() + "/" + "logs" + "/"))
    #
    # handler = TimedRotatingFileHandler(os.path.join(os.getcwd() + "/" + "logs" + "/" + "flask.log") , when='midnight', interval=1, backupCount=7)
    handler = TimedRotatingFileHandler("flask.log" , when='midnight', interval=1, backupCount=7)

    # Set the format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Get the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the logging level to INFO
    logger.addHandler(handler)  # Add the handler to the logger


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
if log_enabled:
    @app.after_request
    def after_request(response):
        # TODO Why does this get the incorrect time on the VPS? Try to fix that.
        timestamp = strftime('[%Y-%b-%d %H:%M]')
        # https://stackoverflow.com/questions/15670763/strftime-gets-wrong-date
        # timestamp = strftime('[%a, %d %b %Y %I:%M:%S %p %Z]')

        # This gets the response without the message, strips the 'OK' or other messages
        string_response = str.split(response.status)[0]

        # Ok or not modified
        if string_response == "200" or string_response == "304":
            logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
            request.full_path, response.status)
        else:
            logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
                         request.full_path, response.status)
        return response

#-----------------

#-----------------
# Add favicon route
#-----------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#-----------------
# Pages
#-----------------

@app.route("/")
def index():
    # client_ip = request.remote_addr
    # Check for the forwarded header first
    client_ip = request.headers.get('X-Forwarded-For')

    # If it's not available, fallback to the remote address
    if client_ip is None:
        client_ip = request.remote_addr
    logging.info(f"Request from IP: {client_ip}")

    return render_template("index.html")
    # return render_template("index.html", password=password_gen(20))

# if passwordGenEnabled:
#     @app.route("/passwordgen")
#     def password_gen_test():
#         return password_gen(20)

#-----------------
# Error pages
#-----------------

# 403 access denied
@app.errorhandler(403)
def access_denied(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(404)
# 404 not found
def not_found(error):
    return render_template("errors/404.html"), 404

# 429 Rate limited
@app.errorhandler(429)
def ratelimit_error(error):
    return render_template('errors/429.html'), 429

#-----------------
# Test pages
#-----------------
if password_gen_enabled:
    @app.route("/password_gen")
    def password_gen_page():
        return render_template("password_gen.html", passwords=password_gen(20))

#-----------------
# End test pages
#-----------------

# This now is supposed to be run with waitress installed like this:
# waitress-serve --port 81 flask_web:app
# I enabled app.run again for testing.
if __name__ == '__main__':
    # setup_app()
    app.run(host='0.0.0.0', port=8081, debug=True)
else:
    # Use Waitress to serve flask web when not running directly
    serve(app, host='0.0.0.0', port=81)  # Production server
