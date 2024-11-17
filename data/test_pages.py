from flask import Blueprint, render_template

# This works for splitting the page into multiple files.
# https://stackoverflow.com/questions/11994325/how-to-divide-flask-app-into-multiple-py-files

simple_page = Blueprint('simple_page', __name__, template_folder='templates')

# Test page, replaced nodejs link with this on the flask server.
# @simple_page.route('/test')
# def test_page():
#     return render_template("test.html")
#
# @simple_page.route('/hello')
# def hello_page():
#     return render_template("hello.html")

# I'm not sure how to get the below working.
# @app.route("/test", methods=['GET'])
# def test_page():
#     return render_template("test.html")
