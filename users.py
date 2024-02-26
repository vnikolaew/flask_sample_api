import os

from flask import Blueprint, abort, url_for
from sqlalchemy import create_engine

from services.user_service import UserService

users = Blueprint('users', __name__, url_prefix='/users')
engine = create_engine(os.environ.get("DB_URL", "sqlite:///social-media.db"), echo=True)


@users.get('/<int:user_id>')
def get_user(user_id: int):
    with UserService(engine) as user_service:
        user = user_service.get_user(user_id)
        if user is None:
            abort(404)

        return user._asdict, 200


@users.get('/')
def get_user_summaries():
    with UserService(engine) as user_service:
        user_summaries = user_service.get_user_summaries()
        return user_summaries


@users.get('/<int:user_id>/feed')
def get_user_feed(user_id: int):
    with UserService(engine) as user_service:
        user_feed = user_service.get_user_feed(user_id=user_id)
        for feed_entry in user_feed:
            feed_entry['post_url'] = url_for('posts.get_post', post_id=feed_entry['post_id'])
        return {'count': len(user_feed), 'items': list(user_feed)}



@users.get('/<int:user_id>/follows/suggestions')
def get_user_follow_suggestions(user_id: int):
    with UserService(engine) as user_service:
        user_follow_suggestions = user_service.get_user_follow_suggestions(user_id)
        return user_follow_suggestions


@users.errorhandler(404)
@users.errorhandler(405)
def handle_error(e):
    return e
