# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import common_pb2 as common__pb2
from . import talk_pb2 as talk__pb2


class ListenStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetListenMetadata = channel.unary_unary(
                '/mobot.Listen/SetListenMetadata',
                request_serializer=common__pb2.Empty.SerializeToString,
                response_deserializer=common__pb2.Success.FromString,
                )
        self.NewListenData = channel.unary_unary(
                '/mobot.Listen/NewListenData',
                request_serializer=talk__pb2.Message.SerializeToString,
                response_deserializer=common__pb2.Success.FromString,
                )


class ListenServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SetListenMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NewListenData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ListenServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetListenMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.SetListenMetadata,
                    request_deserializer=common__pb2.Empty.FromString,
                    response_serializer=common__pb2.Success.SerializeToString,
            ),
            'NewListenData': grpc.unary_unary_rpc_method_handler(
                    servicer.NewListenData,
                    request_deserializer=talk__pb2.Message.FromString,
                    response_serializer=common__pb2.Success.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mobot.Listen', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Listen(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SetListenMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mobot.Listen/SetListenMetadata',
            common__pb2.Empty.SerializeToString,
            common__pb2.Success.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NewListenData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mobot.Listen/NewListenData',
            talk__pb2.Message.SerializeToString,
            common__pb2.Success.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)