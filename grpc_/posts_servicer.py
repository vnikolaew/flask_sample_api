from sqlalchemy import Engine

from __generated__ import posts_pb2_grpc
import __generated__.posts_pb2 as messages
from __generated__.posts_pb2_grpc import add_PostsServiceServicer_to_server
from services.post_service import PostService
from utils import unix_time_millis


class PostsServicer(posts_pb2_grpc.PostsServiceServicer):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def add_to_server(self, server):
        add_PostsServiceServicer_to_server(self, server)

    def GetPostComments(self, request: messages.GetPostCommentsRequest, context) -> messages.GetPostCommentsResponse:
        with PostService(self.engine) as post_service:
            post_comments = post_service.get_post_comments(request.post_id)
            return messages.GetPostCommentsResponse(
                count=len(post_comments),
                items=[messages.GetPostCommentResponse(
                    author_id=comment['author_id'],
                    post_id=comment['post_id'],
                    comment_id=comment['comment_id'],
                    content=comment['content'],
                    timestamp=unix_time_millis(comment['timestamp'].to_pydatetime()),
                    timestamp_relative=comment['timestamp_relative'],
                    comment_likes_count=comment['comment_likes_count'],
                ) for comment in post_comments]
            )

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
