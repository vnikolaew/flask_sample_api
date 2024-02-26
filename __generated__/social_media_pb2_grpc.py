# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import social_media_pb2 as social__media__pb2


class SocialMediaStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUser = channel.unary_unary(
                '/social_media.SocialMedia/GetUser',
                request_serializer=social__media__pb2.GetUserRequest.SerializeToString,
                response_deserializer=social__media__pb2.GetUserResponse.FromString,
                )


class SocialMediaServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SocialMediaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=social__media__pb2.GetUserRequest.FromString,
                    response_serializer=social__media__pb2.GetUserResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'social_media.SocialMedia', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SocialMedia(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/social_media.SocialMedia/GetUser',
            social__media__pb2.GetUserRequest.SerializeToString,
            social__media__pb2.GetUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
