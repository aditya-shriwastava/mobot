import time

import mobot._proto.common_pb2 as common_pb2
import mobot._proto.connection_pb2 as pb2
import mobot._proto.connection_pb2_grpc as pb2_grpc

class FakeSpine(pb2_grpc.ConnectionServicer):
    def Ping(self, _, context):
        return common_pb2.Empty()

    def AttachBrainStream(self, _, context):
        yield pb2.URI(uri = "ipv4:192.168.43.21:43521")
        return
