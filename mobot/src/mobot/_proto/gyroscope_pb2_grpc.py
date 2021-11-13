# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import common_pb2 as common__pb2
from . import imu_pb2 as imu__pb2


class GyroscopeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetGyroscopeMetadata = channel.unary_unary(
                '/mobot.Gyroscope/SetGyroscopeMetadata',
                request_serializer=imu__pb2.SensorMetadata.SerializeToString,
                response_deserializer=common__pb2.Success.FromString,
                )
        self.NewGyroscopeData = channel.unary_unary(
                '/mobot.Gyroscope/NewGyroscopeData',
                request_serializer=common__pb2.Vector3.SerializeToString,
                response_deserializer=common__pb2.Success.FromString,
                )


class GyroscopeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SetGyroscopeMetadata(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NewGyroscopeData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GyroscopeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetGyroscopeMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.SetGyroscopeMetadata,
                    request_deserializer=imu__pb2.SensorMetadata.FromString,
                    response_serializer=common__pb2.Success.SerializeToString,
            ),
            'NewGyroscopeData': grpc.unary_unary_rpc_method_handler(
                    servicer.NewGyroscopeData,
                    request_deserializer=common__pb2.Vector3.FromString,
                    response_serializer=common__pb2.Success.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mobot.Gyroscope', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Gyroscope(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SetGyroscopeMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mobot.Gyroscope/SetGyroscopeMetadata',
            imu__pb2.SensorMetadata.SerializeToString,
            common__pb2.Success.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NewGyroscopeData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mobot.Gyroscope/NewGyroscopeData',
            common__pb2.Vector3.SerializeToString,
            common__pb2.Success.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)