from sqlalchemy import Engine
from sqlalchemy.orm import Session

from __generated__ import social_media_pb2_grpc
import __generated__.social_media_pb2 as messages
from __generated__.social_media_pb2_grpc import add_SocialMediaServicer_to_server
from db.models import User


class SocialMediaServicer(social_media_pb2_grpc.SocialMediaServicer):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def add_to_server(self, server):
        add_SocialMediaServicer_to_server(self, server)

    def GetUser(self, request: messages.GetUserRequest, context):
        with Session(self.engine) as session:
            user = session.query(User).where(User.user_id == request.user_id).first()
            if user is None:
                return messages.GetUserResponse(found=False)

        return messages.GetUserResponse(user=messages.User(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            join_date=user.join_date,
            bio=user.bio,
            profile_picture_url=user.profile_picture_url
        ))
