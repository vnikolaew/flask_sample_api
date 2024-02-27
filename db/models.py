import datetime
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, inspect


class Base(DeclarativeBase):
    @property
    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))
    join_date: Mapped[datetime.datetime] = mapped_column(DateTime())
    bio: Mapped[str] = mapped_column(String(500))
    profile_picture_url: Mapped[str] = mapped_column(String(200))

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan",
        uselist=True, collection_class=list)

    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan",
        uselist=True, collection_class=list)

    likes: Mapped[List["PostLike"]] = relationship(
        "PostLike", back_populates="user", cascade="all, delete-orphan",
        uselist=True, collection_class=list)

    following: Mapped[List["Follow"]] = relationship(
        "Follow", back_populates="follower_user", cascade="all, delete",
        foreign_keys="Follow.follower_user_id"
    )

    followers: Mapped[List["Follow"]] = relationship(
        "Follow", back_populates="following_user", cascade="all, delete",
        foreign_keys="Follow.following_user_id"
    )


class Post(Base):
    __tablename__ = 'posts'

    post_id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")

    content: Mapped[str] = mapped_column(String(300))
    post_date: Mapped[datetime.datetime] = mapped_column(DateTime())

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="post", cascade='all, delete-orphan')
    likes: Mapped[List["PostLike"]] = relationship("PostLike", back_populates="post", cascade='all, delete-orphan')


class Comment(Base):
    __tablename__ = 'comments'

    comment_id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.post_id"))
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="comments")

    content: Mapped[str] = mapped_column(String(300))
    comment_date: Mapped[datetime.datetime] = mapped_column(DateTime())

    likes: Mapped[List["CommentLike"]] = relationship(
        "CommentLike", back_populates="comment",
        cascade='all, delete-orphan')


@dataclass
class PostLike(Base):
    __tablename__ = 'post_likes'

    like_id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.post_id"))
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User", back_populates="likes")

    like_date: Mapped[datetime.datetime] = mapped_column(DateTime())


@dataclass
class CommentLike(Base):
    __tablename__ = 'comment_likes'

    like_id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.comment_id"))
    comment: Mapped["Comment"] = relationship("Comment", back_populates="likes")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship("User")

    like_date: Mapped[datetime.datetime] = mapped_column(DateTime())


class Follow(Base):
    __tablename__ = 'follows'

    follow_id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    follower_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    follower_user: Mapped[User] = relationship("User", back_populates="following", foreign_keys=[follower_user_id])

    following_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    following_user: Mapped[User] = relationship("User", back_populates="followers", foreign_keys=[following_user_id])

    follow_date: Mapped[datetime.datetime] = mapped_column(DateTime())
