# Logger
import logging
# Time for logging
from time import strftime

from flask import Flask, url_for, request, render_template, jsonify, redirect, make_response
from flask_cors import CORS, cross_origin

# import pymysql
import os
from os.path import join, dirname
from dotenv import load_dotenv

from test_pages import simple_page
from password_gen import password_gen

###
# Downloads page
from downloads import downloads
# Form test page
from form_test import form_test

# TODO Look into this later: https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript


# Setup .env file for database password
# https://stackoverflow.com/questions/41546883/what-is-the-use-of-python-dotenv
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Todo Re-enable the database once I have it setup on the server.
# Disabled the database for testing.

# I used a part of the below guide for some of these values
# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# database_host = os.environ.get("DATABASE_HOST")
# database_username = os.environ.get("DATABASE_USERNAME")
# database_password = os.environ.get("DATABASE_PASSWORD")
# database_name = os.environ.get("DATABASE_NAME")

# The app.config string needed to be changed to "mysql+pymysql://" to work
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
# Set up the app, login manager and database
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
app.register_blueprint(form_test)

app.secret_key= os.environ.get("SECRET_KEY")
# Create the SQLAlchemy instance
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{database_username}:{database_password}@{database_host}/{database_name}"
# app.config["SQLALCHEMY_DATABASE_URI"] = """f
# "mysql+pymysql://{database_username}:{database_password}@{database_host}/{database_name}"
# """
# db = SQLAlchemy(app)
# db = pymysql.connect(host=database_host, user=database_username, password=database_password, database=database_name)


# Setup logging
# https://github.com/google/openhtf/issues/46
# https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module

# This toggles the logging to file on and off, useful for debugging without writing to the logs.
logEnabled = True
if logEnabled:
    log_file = "flask.log"
    logging.basicConfig(filename=log_file, filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


# # https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask

# https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
# def sql_results():
#     # https://stackoverflow.com/questions/9845102/using-mysql-in-flask
#     cur = db.cursor()
#     sql = "SELECT * FROM passwords"
#     cur.execute(sql)
#     results = cur.fetchall()

#     # This works without the [] but it only displays one password
#     # This works fine in the mariadb_test and prints the items to the console
#     # for [item] in results:
#         # return item

#     return results

###
# Logging
###

# https://stackoverflow.com/questions/52372187/logging-with-command-line-waitress-serve
# https://flask.palletsprojects.com/en/2.3.x/logging/
# Test
# This seems to log everything with errors


# Disable this for local network for testing.
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

####

###
# Pages
###

@app.route("/")
def index():
    # return render_template("index.html", password=password_gen(20))
    return render_template("index.html", password=password_gen(20))

@app.route("/passwordgen")
def password_gen_test():
    return password_gen(20)

# Todo Figure out how to get values out of a database using this.
# @app.route("/var_test", methods = ['GET'])
# def test1_page():
#     if request.method == 'GET':
#         # data = "Test"
#         data = {'username': 'admin', 'site': 'kelsoncraft.net'}
#         return render_template("var_test.html", data=data)
        # return jsonify({'data': data})

#////////////////
# About pages
#////////////////

# Todo Fix this to redirect to about.html
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


# ////////////////
# End about pages
# ////////////////

# ////////////////
# Video pages
# ////////////////

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


# ////////////////
# End video pages
# ////////////////

@app.route("/password_gen")
def password_gen_page():
    return render_template("password_gen.html", passwords=password_gen(20))

#////////////////
# Test pages
#////////////////
# This one isn't ready to be published yet
# @app.route("/fivem_test")
# @cross_origin()
# def fivem_test_page():
#     return render_template("fivem-test.html")

# ////////////////
# End test pages
# ////////////////

# This now is supposed to be run with waitress installed like this:
# waitress-serve --port 81 flask_web:app
# I enabled app.run again for testing.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
