import logging

from flask import Blueprint, render_template, abort, send_from_directory, current_app, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from models import User, bcrypt

login_pages = Blueprint('login_pages', __name__, template_folder='templates')

import logging

# Import the logger
logger = logging.getLogger()

#### Auth Test
# I got this working, added SQLite password salting/hashing
# Moved out of video_pages.py

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# TODO Add IP logging for when a user logs in, or if a login is failed
# TODO Setup rate limiting, limit logins to 10 per minute.
# TODO Fix the redirect when going to a specific page, so if I'm on video 4,
#  redirect to video 4, currently it doesn't work like that.
@login_pages.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()  # Create an instance of the form

    next_video = session.pop('next', url_for('video_pages.video_main_page'))

    if form.validate_on_submit():  # Validate the form input
        username = form.username.data  # Access form data
        plain_password = form.password.data

        user = User.query.filter_by(username=username).first()
        user_ip = request.remote_addr

        if user and bcrypt.check_password_hash(user.password, plain_password):
            session['user_id'] = user.id
            login_user(user)

            logger.info(f"Successful login for user: {username} from IP: {user_ip}")
            # print(f"Successful login for user: '{username}' from IP: {user_ip}")
            flash('Login Successful!', 'success')
            return redirect(next_video)
        else:

            logger.info(f"Login failed for user: '{username}' from IP: {user_ip}")
            # print(f"Login failed for user: '{username}' from IP: {user_ip}")
            flash('Login Failed. Please check your credentials.', 'danger')

    return render_template('login.html', form=form)  # Pass the form to the template

@login_pages.route('/logout')
@login_required
def logout():
    # session.pop('user_id', None)

    # return redirect(url_for('login_pages.login'))
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login_pages.login'))

####