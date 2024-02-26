from typing import Optional

import arrow
from sqlalchemy import Engine

import pandas as pd
from db.models import Post, Like, Comment, User
from services.service_base import ServiceBase


class PostService(ServiceBase):
    def __init__(self, engine: Engine):
        super().__init__(engine)

    def get_post(self, post_id: int) -> Optional[Post]:
        post = self.session.query(Post).where(Post.post_id == post_id).first()
        return post

    def get_post_comments(self, post_id: int):
        post_comments_query = self.session.query(Comment).where(Comment.post_id == post_id)
        post_comments_df = pd.read_sql_query(post_comments_query.statement, self.session.bind)
        comments = post_comments_df.sort_values(
            by=['comment_date'],
            ascending=False).rename(
            columns={'comment_date': 'timestamp', 'user_id': 'author_id'})
        comments['timestamp_relative'] = comments['timestamp'].apply(lambda dt: arrow.get(dt).humanize(arrow.utcnow()))

        return comments.to_dict('records')

    def get_post_summaries(self):
        post_query = self.session.query(Post).limit(100)
        posts_df = pd.read_sql_query(post_query.statement, self.session.bind)

        likes_query = self.session.query(Like.like_id, Like.post_id)
        likes_df = pd.read_sql_query(likes_query.statement, likes_query.session.bind)

        comments_query = self.session.query(Comment.comment_id, Comment.post_id)
        comments_df = pd.read_sql_query(comments_query.statement, comments_query.session.bind)

        users_query = self.session.query(User.user_id, User.username, User.email)
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
