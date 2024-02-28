from sqlalchemy import Engine

import __generated__.users_pb2 as messages
from __generated__ import users_pb2_grpc
from __generated__.users_pb2_grpc import add_UsersServiceServicer_to_server
from services.user_service import UserService
from utils import unix_time_millis


class UsersServicer(users_pb2_grpc.UsersServiceServicer):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def add_to_server(self, server):
        add_UsersServiceServicer_to_server(self, server)


    def GetUser(self, request: messages.GetUserRequest, context):
        with UserService(self.engine) as user_service:
            user = user_service.get_user(request.user_id)
            if user is None:
                return messages.GetUserResponse(found=False)

            return messages.GetUserResponse(found=True, user=messages.User(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                join_date_timestamp=unix_time_millis(user.join_date),
                bio=user.bio,
                profile_picture_url=user.profile_picture_url
            ))

    def GetUserSummaries(self, request: messages.GetUserSummariesRequest, context):
        with UserService(self.engine) as user_service:
            user_summaries: dict[any, any] = user_service.get_user_summaries()

            user_summary_responses: list[messages.GetUserSummaryResponse] = []
            for user_summary in user_summaries['items']:
                user_summary_responses.append(messages.GetUserSummaryResponse(
                    user=messages.User(
                        user_id=user_summary['user_id'],
                        username=user_summary['username'],
                        email=user_summary['email'],
                        join_date_timestamp=unix_time_millis(user_summary['join_date']),
                        bio=user_summary['bio'],
                        profile_picture_url=user_summary['profile_picture_url']
                    ),
                    followers=messages.UserFollowersResponse(
                        count=1,
                        items=[messages.UserFollowerResponse(**follower) for follower in
                               user_summary['followers']['items']])))

            return messages.GetUserSummariesResponse(count=user_summaries['count'], items=user_summary_responses)
