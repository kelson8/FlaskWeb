from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Moved user models into here

db = SQLAlchemy()
bcrypt = Bcrypt()

# Disable the password generator for now.
password_gen_enabled = False

# Toggle logging on/off here, if off it redirects log output to the console in PyCharm.
log_enabled = True

# TODO Fix this, this is incomplete.
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     role = db.Column(db.String(50), default='user')


class User(UserMixin):
    def __init__(self, id):
        self.id = id

# This is very insecure, switch to password hashing with salt in SQLite.
users = {'admin': 'password'}
