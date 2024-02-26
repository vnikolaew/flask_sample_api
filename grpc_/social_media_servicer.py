from sqlalchemy import Engine

import __generated__.social_media_pb2 as messages
from __generated__ import social_media_pb2_grpc
from services.post_service import PostService
from services.user_service import UserService
from utils import unix_time_millis


class SocialMediaServicer(social_media_pb2_grpc.SocialMediaServicer):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def add_to_server(self, server):
        social_media_pb2_grpc.add_SocialMediaServicer_to_server(self, server)

    def GetPost(self, request: messages.GetPostRequest, context):
        with PostService(self.engine) as post_service:
            post = post_service.get_post(request.post_id)
            if post is None:
                return messages.GetPostResponse(found=False)

            return messages.GetPostResponse(found=True, post=messages.Post(
                user_id=post.user_id,
                post_id=post.post_id,
                post_date_timestamp=unix_time_millis(post.post_date),
                content=post.content
            ))

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
