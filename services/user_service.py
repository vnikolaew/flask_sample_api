import arrow
from sqlalchemy import Engine
from typing import Optional
import pandas as pd

from db.models import User, Follow, Post
from services.service_base import ServiceBase


class UserService(ServiceBase):
    engine: Engine

    def __init__(self, engine: Engine):
        super().__init__(engine)

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by its ID
        :param user_id: The User ID provided
        """

        user = self.session.query(User).where(User.user_id == user_id).first()
        return user

    def get_user_feed(self, user_id: int) -> list[dict[str, any]]:
        following_query = self.session.query(Follow.following_user_id).where(Follow.follower_user_id == user_id)
        following_users_df = pd.read_sql_query(following_query.statement, self.session.bind)

        following_users_ids = list(following_users_df['following_user_id'].unique())

        following_users_posts = self.session.query(Post).where(
            Post.user_id.in_([int(user_id) for user_id in following_users_ids]))
        following_users_posts_df = pd.read_sql_query(following_users_posts.statement, self.session.bind)
        feed: pd.DataFrame = following_users_posts_df.sort_values(by=['post_date'], ascending=False).iloc[:100]

        feed = feed.rename(columns={'user_id': 'author_id', 'post_date': 'timestamp'})
        feed['timestamp_relative'] = feed['timestamp'].apply(lambda dt: arrow.get(dt).humanize(arrow.utcnow()))

        return feed.to_dict(orient='records')

    def get_user_summaries(self):
        users_query = self.session.query(User).limit(100)
        users_df = pd.read_sql_query(users_query.statement, self.session.bind)

        follows_query = self.session.query(Follow.following_user_id, Follow.follower_user_id, Follow.follow_id)
        follower_groups_df = pd.read_sql_query(follows_query.statement, self.session.bind).groupby('following_user_id')

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

    def get_user_follow_suggestions(self, user_id: int):
        follows_query = self.session.query(Follow).where(Follow.following_user_id == user_id)
        followers_df = pd.read_sql_query(follows_query.statement, self.session.bind)

        # Get user followers:
        follower_ids_set = set(followers_df['follower_user_id'].unique())

        # For each follower, get their followers as well:
        followers_query = self.session.query(Follow).where(
            Follow.follower_user_id.in_([int(follower_id) for follower_id in list(follower_ids_set)]))

        followers_df = pd.read_sql_query(followers_query.statement, self.session.bind)
        follower_followings_ids_set = set(followers_df['following_user_id'].unique())

        follow_suggestions: set[int] = follower_followings_ids_set.difference(follower_ids_set)
        return {'follow_suggestions': follow_suggestions}
