import os

import pandas as pd
from flask import Blueprint, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import User, Follow

users = Blueprint('users', __name__, url_prefix='/users')
engine = create_engine(os.environ.get("DB_URL", "sqlite:///social-media.db"), echo=True)


@users.get('/<int:user_id>')
def get_user(user_id: int):
    with Session(engine) as session:
        user = session.query(User).where(User.user_id == user_id).first()
        if user is None:
            abort(404)

    return user._asdict, 200


@users.get('/')
def get_user_summaries():
    with Session(engine) as session:
        users_query = session.query(User).limit(100)
        users_df = pd.read_sql_query(users_query.statement, session.bind)

        follows_query = session.query(Follow.following_user_id, Follow.follower_user_id, Follow.follow_id)
        follower_groups_df = pd.read_sql_query(follows_query.statement, session.bind).groupby('following_user_id')

        users_dict = users_df.to_dict('index')
        for index in users_dict:
            users_dict[index]['followers'] = {'items': [], 'count': 0}

        for user_id, follower_group in follower_groups_df:
            if user_id in users_dict:
                follower_ids: list[int] = follower_group['follower_user_id'].values
                follower_ids.sort()
                followers = [users_dict[follower_id] if follower_id in users_dict else None
                             for follower_id in follower_ids]

                for follower in [f for f in followers if f is not None]:
                    users_dict[user_id]['followers']['items'].append(
                        {'follower_id': follower['user_id'], 'email': follower['email'],
                         'username': follower['username']})
                    users_dict[user_id]['followers']['count'] += 1

        return {'count': len(users_dict), 'items': list(users_dict.values())}


@users.get('/<int:user_id>/follows/suggestions')
def get_user_follow_suggestions(user_id: int):
    with Session(engine) as session:
        follows_query = session.query(Follow).where(Follow.following_user_id == user_id)
        followers_df = pd.read_sql_query(follows_query.statement, session.bind)

        # Get user followers:
        follower_ids_set = set(followers_df['follower_user_id'].unique())

        # For each follower, get their followers as well:
        followers_query = session.query(Follow).where(
            Follow.follower_user_id.in_([int(follower_id) for follower_id in list(follower_ids_set)]))

        followers_df = pd.read_sql_query(followers_query.statement, session.bind)
        follower_followings_ids_set = set(followers_df['following_user_id'].unique())

        follow_suggestions: set[int] = follower_followings_ids_set.difference(follower_ids_set)
        return {'follow_suggestions': follow_suggestions}


@users.errorhandler(404)
@users.errorhandler(405)
def handle_error(e):
    return e
