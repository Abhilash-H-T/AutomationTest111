import os
from datetime import timedelta
from redis import Redis

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SESSION_COOKIE_NAME = 'your_session_cookie'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Session timeout after 30 minutes of inactivity
    SESSION_TYPE = 'filesystem'  # Or 'redis' / 'memcached' depending on your choice
    SESSION_USE_SIGNER = True  # Sign the cookie to prevent tampering
    SQLALCHEMY_DATABASE_URI = 'sqlite:///files.db'  # Using SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'log'}
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_REDIS = Redis(host='localhost', port=6379)