from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("user_id", "username", "email", "join_date", "profile_picture_url", "bio")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    JOIN_DATE_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    username: str
    email: str
    join_date: _timestamp_pb2.Timestamp
    profile_picture_url: str
    bio: str
    def __init__(self, user_id: _Optional[int] = ..., username: _Optional[str] = ..., email: _Optional[str] = ..., join_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., profile_picture_url: _Optional[str] = ..., bio: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("found", "user")
    FOUND_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    found: bool
    user: User
    def __init__(self, found: bool = ..., user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...
