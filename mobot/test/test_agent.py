import logging
import pytest

from mobot.brain.agent import Agent

from .fake_spine import FakeSpine

import mobot._proto.common_pb2 as common_pb2
import mobot._proto.connection_pb2 as pb2
import mobot._proto.connection_pb2_grpc as pb2_grpc

@pytest.fixture(scope='module')
def grpc_add_to_server():
    return pb2_grpc.add_ConnectionServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    return FakeSpine()

@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    return pb2_grpc.ConnectionStub

class TestFakeSpine:
    def test_ping(self, grpc_stub):
        assert grpc_stub.Ping(common_pb2.Empty()) == common_pb2.Empty()
    def test_attach_brain_stream(self, grpc_stub):
        attach_brain_iterator = grpc_stub.AttachBrainStream(common_pb2.Empty())
        for body in attach_brain_iterator:
            uri = body.uri
            break
        assert uri == "ipv4:192.168.43.21:43521"

class TestAgent:
    @pytest.fixture
    def my_agent(self):
        return Agent()

    def test_start_without_spine(self, my_agent, caplog):
        with pytest.raises(SystemExit) as e:
            my_agent.start()

        assert e.type == SystemExit
        assert caplog.record_tuples == [("root", logging.ERROR, "Unable to attach Brain to Spine!")]

    def test_start_with_spine(self, my_agent, caplog, grpc_stub):
        with pytest.raises(SystemExit) as e:
            my_agent.start()

        assert e.type == SystemExit
        assert caplog.record_tuples == [("root", logging.ERROR, "Unable to attach Brain to Spine!")]

