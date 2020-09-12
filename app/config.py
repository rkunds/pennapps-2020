import os


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SPOTIFY_OAUTH_CLIENT_ID = os.environ.get("SPOTIFY_OAUTH_CLIENT_ID")
    SPOTIFY_OAUTH_CLIENT_SECRET = os.environ.get("SPOTIFY_OAUTH_CLIENT_SECRET")
