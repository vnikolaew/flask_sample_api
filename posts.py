import os

import pandas as pd
from flask import Blueprint, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import Post, Like, Comment, User

posts = Blueprint('posts', __name__, url_prefix='/posts')
engine = create_engine(os.environ.get("DB_URL", "sqlite:///social-media.db"), echo=True)


@posts.get('/<int:post_id>')
def get_post(post_id: int):
    with Session(engine) as session:
        post = session.query(Post).where(Post.post_id == post_id).first()
        if post is None:
            abort(404)

        return post._asdict, 200


@posts.get('/')
def get_post_summaries():
    with Session(engine) as session:
        post_query = session.query(Post).limit(100)
        posts_df = pd.read_sql_query(post_query.statement, session.bind)

        likes_query = session.query(Like.like_id, Like.post_id)
        likes_df = pd.read_sql_query(likes_query.statement, likes_query.session.bind)

        comments_query = session.query(Comment.comment_id, Comment.post_id)
        comments_df = pd.read_sql_query(comments_query.statement, comments_query.session.bind)

        users_query = session.query(User.user_id, User.username, User.email)
        users_df = pd.read_sql_query(users_query.statement, users_query.session.bind)

        groups_df = posts_df.merge(likes_df, on="post_id", how="right").groupby('post_id')
        group_sizes: pd.Series = groups_df.size()

        comments_groups_df = posts_df.merge(comments_df, on="post_id", how="right").groupby('post_id')
        comments_group_sizes: pd.Series = comments_groups_df.size()

        result = posts_df.merge(
            group_sizes.rename("likes_count").to_frame(),
            left_on='post_id',
            right_index=True).merge(
            comments_group_sizes.rename('comments_count').to_frame(),
            left_on='post_id',
            right_index=True).sort_values(by="post_id")

        post_records = result.to_dict("records", index=True)
        for post_record in post_records:
            user = users_df.loc[post_record['user_id']]
            post_record['author'] = {'user_id': int(user.user_id), 'username': user.username, 'email': user.email}

        return {'count': len(post_records), 'items': post_records}
