from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserSummariesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUserSummariesResponse(_message.Message):
    __slots__ = ("count", "items")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    count: int
    items: _containers.RepeatedCompositeFieldContainer[GetUserSummaryResponse]
    def __init__(self, count: _Optional[int] = ..., items: _Optional[_Iterable[_Union[GetUserSummaryResponse, _Mapping]]] = ...) -> None: ...

class GetUserSummaryResponse(_message.Message):
    __slots__ = ("user", "followers")
    USER_FIELD_NUMBER: _ClassVar[int]
    FOLLOWERS_FIELD_NUMBER: _ClassVar[int]
    user: User
    followers: UserFollowersResponse
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., followers: _Optional[_Union[UserFollowersResponse, _Mapping]] = ...) -> None: ...

class UserFollowersResponse(_message.Message):
    __slots__ = ("count", "items")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    count: int
    items: _containers.RepeatedCompositeFieldContainer[UserFollowerResponse]
    def __init__(self, count: _Optional[int] = ..., items: _Optional[_Iterable[_Union[UserFollowerResponse, _Mapping]]] = ...) -> None: ...

class UserFollowerResponse(_message.Message):
    __slots__ = ("follower_id", "username", "email")
    FOLLOWER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    follower_id: int
    username: str
    email: str
    def __init__(self, follower_id: _Optional[int] = ..., username: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class GetPostRequest(_message.Message):
    __slots__ = ("post_id",)
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    def __init__(self, post_id: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("user_id", "username", "email", "join_date_timestamp", "profile_picture_url", "bio")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    JOIN_DATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    username: str
    email: str
    join_date_timestamp: int
    profile_picture_url: str
    bio: str
    def __init__(self, user_id: _Optional[int] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., join_date_timestamp: _Optional[int] = ..., profile_picture_url: _Optional[str] = ..., bio: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ("post_id", "user_id", "content", "post_date_timestamp")
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    POST_DATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    post_id: int
    user_id: int
    content: str
    post_date_timestamp: int
    def __init__(self, post_id: _Optional[int] = ..., user_id: _Optional[int] = ..., content: _Optional[str] = ..., post_date_timestamp: _Optional[int] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("found", "user")
    FOUND_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    found: bool
    user: User
    def __init__(self, found: bool = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class GetPostResponse(_message.Message):
    __slots__ = ("found", "post")
    FOUND_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    found: bool
    post: Post
    def __init__(self, found: bool = ..., post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...
