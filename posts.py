import os

from flask import Blueprint, abort
from sqlalchemy import create_engine

from services.post_service import PostService

posts = Blueprint('posts', __name__, url_prefix='/posts')
engine = create_engine(os.environ.get("DB_URL", "sqlite:///social-media.db"), echo=True)


@posts.get('/<int:post_id>')
def get_post(post_id: int):
    with PostService(engine) as post_service:
        post = post_service.get_post(post_id)
        if post is None:
            abort(404)

        return post._asdict, 200


@posts.get('/')
def get_post_summaries():
    with PostService(engine) as post_service:
        post_summaries = post_service.get_post_summaries()
        return post_summaries
