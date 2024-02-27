from datetime import datetime
from random import randint

from faker import Faker
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session

from db.models import User, Post, Comment, PostLike, Follow, CommentLike, Base
from utils import get_bool_env_variable

DB_SEED = 324235
TRUNCATE_TABLES = get_bool_env_variable('TRUNCATE_TABLES')


def generate_user(faker: Faker) -> User:
    join_date = faker.date_between()
    return User(
        username=faker.name(),
        email=faker.safe_email(),
        join_date=join_date,
        profile_picture_url=faker.image_url(),
        bio=faker.text(200),
        posts=[generate_post(faker, join_date) for _ in range(0, randint(2, 10))]
    )


def generate_post(faker: Faker, start_date: datetime) -> Post:
    return Post(
        content=faker.paragraph(nb_sentences=3),
        post_date=faker.date_between(start_date=start_date),
    )


def generate_comment(faker: Faker, post: Post, users: list[User]) -> Comment:
    user_commenter = users[randint(0, len(users) - 1)]
    return Comment(
        post=post,
        user=user_commenter,
        content=faker.paragraph(nb_sentences=2),
        comment_date=faker.date_between(start_date=post.post_date)
    )


def generate_comment_like(faker: Faker, comment: Comment, users: list[User]) -> CommentLike:
    user_liker = users[randint(0, len(users) - 1)]
    return CommentLike(
        comment=comment,
        user_id=user_liker,
        like_date=faker.date_between(start_date=comment.comment_date)
    )


def generate_like(faker: Faker, post: Post, users: list[User]) -> PostLike:
    user_liker = users[randint(0, len(users) - 1)]
    return PostLike(
        post=post,
        user=user_liker,
        like_date=faker.date_between(start_date=post.post_date)
    )


class DatabaseSeeder:
    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def _seed_users(self, faker: Faker, session: Session):
        # Generate users and posts:
        users = [generate_user(faker) for _ in range(0, 100)]
        session.add_all(users)
        session.commit()

    def _seed_comments(self, users: list[User], faker: Faker, post: Post, session: Session):
        # Generate comments:
        comments = [generate_comment(faker, post, users) for _ in range(0, randint(3, 20))]
        session.add_all(comments)

    def _seed_likes(self, users: list[User], faker: Faker, post: Post, session: Session):
        # Generate comments:
        likes = [generate_like(faker, post, users) for _ in range(0, randint(10, 50))]
        session.add_all(likes)

    def _seed_comment_likes(self, users: list[User], faker: Faker, session: Session):
        # Generate comments:
        comments = session.query(Comment).all()
        for comment in comments:
            likes = [generate_comment_like(faker, comment, users) for _ in range(0, randint(10, 50))]
            session.add_all(likes)

    def _seed_follows(self, faker: Faker, users: list[User], session: Session):
        for user in users:
            for _ in range(0, randint(3, 20)):
                follower = users[randint(0, len(users) - 1)]
                while follower.user_id == user.user_id:
                    follower = users[randint(0, len(users) - 1)]

                follow = Follow(
                    follower_user_id=follower.user_id,
                    following_user_id=user.user_id,
                    follow_date=faker.date_between(start_date=user.join_date))
                session.add(follow)

    def _truncate_tables(self, session: Session):
        all_tables = list(Base.metadata.tables.keys())
        for table in all_tables:
            session.execute(text(f'TRUNCATE TABLE IF EXISTS {0};'.format(table)))

    def __call__(self) -> None:
        faker = Faker()
        Faker.seed(DB_SEED)

        with Session(self.engine) as session:
            count = session.query(User.user_id).count()

            if TRUNCATE_TABLES:
                self._truncate_tables(session)

            # Generate users and posts:
            if count == 0:
                self._seed_users(faker, session)

        with Session(self.engine) as session:
            users = session.query(User).all()
            posts = session.query(Post).all()

            # Generate comments and likes:
            for post in posts:
                comments_count = session.query(Comment).count()
                if comments_count == 0:
                    self._seed_comments(users, faker, post, session)

                likes_count = session.query(PostLike).count()
                if likes_count == 0:
                    self._seed_likes(users, faker, post, session)

                session.commit()

                comment_likes_count = session.query(CommentLike).count()
                if comment_likes_count == 0:
                    self._seed_comment_likes(users, faker, session)

            # Generate follows:
            follows_count = session.query(Follow).count()
            if follows_count == 0:
                self._seed_follows(faker, users, session)

            session.commit()
