from flask import Flask, url_for, request, render_template, jsonify, redirect
from flask_cors import CORS, cross_origin

# import pymysql
import os
from os.path import join, dirname
from dotenv import load_dotenv

from test_pages import simple_page
from password_gen import password_gen

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

app.secret_key= os.environ.get("SECRET_KEY")
# Create the SQLAlchemy instance
# app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{database_username}:{database_password}@{database_host}/{database_name}"
# app.config["SQLALCHEMY_DATABASE_URI"] = """f
# "mysql+pymysql://{database_username}:{database_password}@{database_host}/{database_name}"
# """
# db = SQLAlchemy(app)
# db = pymysql.connect(host=database_host, user=database_username, password=database_password, database=database_name)


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

@app.route("/")
def index():
    # return render_template("index.html", password=password_gen(20))
    return render_template("index.html", password=password_gen(20))

@app.route("/passwordgen")
def password_gen_test():
    return password_gen(20)

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

# ////////////////
# End about pages
# ////////////////

@app.route("/password_gen")
def password_gen_page():
    return render_template("password_gen.html", passwords=password_gen(20))

# @app.route("/db_test")
# def db_test_page():
#     return render_template("db_test.html", results=sql_results())

# Types that can be used in the @app.route
# String Text without a slash
# Int Positive integers
# Float Postive floating point values.
# Path Like string but also accepts slashes.
# UUID Accepts UUID strings

# This now is supposed to be run with waitress installed like this:
# waitress-serve --port 81 flask_web:app
if __name__ == '__main__':
    pass
    # app.run(host='0.0.0.0', port=81, debug=True)
