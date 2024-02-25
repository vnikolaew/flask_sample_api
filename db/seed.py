from datetime import datetime
from random import randint

from faker import Faker
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from db.models import User, Post, Comment, Like, Follow

DB_SEED = 324235


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


def generate_like(faker: Faker, post: Post, users: list[User]) -> Like:
    user_liker = users[randint(0, len(users) - 1)]
    return Like(
        post=post,
        user=user_liker,
        like_date=faker.date_between(start_date=post.post_date)
    )


class DatabaseSeeder:
    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def __call__(self) -> None:
        faker = Faker()
        Faker.seed(DB_SEED)

        with Session(self.engine) as session:
            count = session.query(User.user_id).count()

            # Generate users and posts:
            if count == 0:
                users = [generate_user(faker) for _ in range(0, 100)]
                session.add_all(users)
                session.commit()

        with Session(self.engine) as session:
            users = session.query(User).all()
            posts = session.query(Post).all()

            # Generate comments and likes:
            for post in posts:
                comments_count = session.query(Comment).count()
                if comments_count == 0:
                    comments = [generate_comment(faker, post, users) for _ in range(0, randint(3, 20))]
                    session.add_all(comments)

                likes_count = session.query(Like).count()
                if likes_count == 0:
                    likes = [generate_like(faker, post, users) for _ in range(0, randint(10, 50))]
                    session.add_all(likes)

            # Generate follows:
            follows_count = session.query(Follow).count()
            if follows_count == 0:
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

            session.commit()
