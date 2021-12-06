# MIT License
#
# Copyright (c) 2021 Mobotx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .abstract.actuator import Actuator

import mobot._proto.chassis_pb2 as pb2
import mobot._proto.chassis_pb2_grpc as pb2_grpc


class Chassis(pb2_grpc.ChassisServicer, Actuator):

    def __init__(self, logger, connection):
        Actuator.__init__(self, logger, connection)
        self.WHEEL_DIAMETER = None
        self.WHEEL_TO_WHEEL_SEPERATION  = None
        self.MAX_WHEEL_SPEED = None
        self.MIN_WHEEL_SPEED = None

    ## Private method (used for grpc communication)
    def ChassisCmdStream(self, chassis_metadata, context):
        for cmd in self._actuator_cmd_stream(chassis_metadata, context):
            yield cmd

    def _set_metadata(self, metadata):
        self.WHEEL_DIAMETER = metadata.WHEEL_DIAMETER
        self.WHEEL_TO_WHEEL_SEPERATION = metadata.WHEEL_TO_WHEEL_SEPERATION
        self.MAX_WHEEL_SPEED = metadata.MAX_WHEEL_SPEED
        self.MIN_WHEEL_SPEED = metadata.MIN_WHEEL_SPEED

    def _reset_metadata(self):
        self.WHEEL_DIAMETER = None
        self.WHEEL_TO_WHEEL_SEPERATION = None
        self.MAX_WHEEL_SPEED = None
        self.MIN_WHEEL_SPEED = None

    def set_wheel_velocity(self, wr=0.0, wl=0.0, blocking=True):
        if self.available:
            self._new_cmd(pb2.CmdVel(wr=wr, wl=wl), blocking=blocking)
        return self.available

    def set_cmdvel(self, v=0.0, w=0.0, blocking=True):
        if self.available:
            wr, wl = self.__inverse_kinematics(v, w)
            self._new_cmd(pb2.CmdVel(wr=wr, wl=wl), blocking=blocking)
        return self.available

    def __inverse_kinematics(self, v, w):
        wr = -(1/(self.WHEEL_DIAMETER/2)) * (v + (w * (self.WHEEL_TO_WHEEL_SEPERATION/2)))
        wl = (1/(self.WHEEL_DIAMETER/2)) * (v - (w * (self.WHEEL_TO_WHEEL_SEPERATION/2)))
        return wr, wl
