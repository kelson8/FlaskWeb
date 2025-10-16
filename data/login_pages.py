
from flask import Blueprint, render_template, abort, send_from_directory, current_app, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from models import User, bcrypt

login_pages = Blueprint('login_pages', __name__, template_folder='templates')

#### Auth Test
# I got this working, added SQLite password salting/hashing
# Moved out of video_pages.py

# TODO Add IP logging for when a user logs in, or if a login is failed
# TODO Setup rate limiting, limit logins to 10 per minute.
# TODO Fix the redirect when going to a specific page, so if I'm on video 4,
#  redirect to video 4, currently it doesn't work like that.
@login_pages.route('/login', methods=['GET', 'POST'])
def login():
    # Get next video URL to redirect to after login
    next_video = session.pop('next', url_for('video_pages.video_main_page'))

    if request.method == 'POST':
        username = request.form['username']
        plain_password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, plain_password):
            session['user_id'] = user.id
            login_user(user)

            # print("Redirecting to: ", next_video)

            flash('Login Successful!', 'success')
            return redirect(next_video)
        else:
            flash('Login Failed. Please check your credentials.', 'danger')

    return render_template('login.html')

# @login_pages.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users and users[username] == password:
#             user = User(username)
#             login_user(user)
#             return redirect(url_for('video_pages.video_main_page'))
#         flash('Invalid username or password.')
#     return render_template('login.html')
#
@login_pages.route('/logout')
@login_required
def logout():
    # session.pop('user_id', None)

    # return redirect(url_for('login_pages.login'))
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_pages.login'))

####