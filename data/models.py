from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

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

# User model for the SQLite DB
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')

