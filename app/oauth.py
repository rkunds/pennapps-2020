from flask import flash
from flask_login import current_user, login_user
from flask_dance.contrib.spotify import make_spotify_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from models import db, User, OAuth


blueprint = make_spotify_blueprint(
    scope="user-read-email user-read-private user-read-playback-state user-read-currently-playing",
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)


@oauth_authorized.connect_via(blueprint)
def spotify_logged_in(blueprint, token):
    if not token:
        msg = "Failed to log in."
        flash(msg, category="error")
        return False

    resp = blueprint.session.get("/v1/me")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = resp.json()
    user_id = info["id"]

    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")

    else:
        user = User(email=info["email"], display_name=info["display_name"])
        oauth.user = user

        db.session.add_all([user, oauth])
        db.session.commit()

        login_user(user)
        flash("Successfully signed in.")

    return False


@oauth_error.connect_via(blueprint)
def spotify_error(blueprint, message, response):
    msg = f"OAuth error from {blueprint.name}! message={message} response={response}"
    flash(msg, category="error")
