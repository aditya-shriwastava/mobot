import math
from machine import Timer

from libs.motor import Motor
from libs.encoder import MonoDirEncoder
from libs.led import Led
from libs.joint_state import JointState
from mobot_data import *

class MotorEncoderAssemblyTest:
    def __init__(self):
        self.dled = Led(DLED)
        self.motor = Motor(MR_CHA, MR_CHB, MIN_OPR)
        self.motor.set_cmd(0)
        self.encoder = MonoDirEncoder(ER_CHA, ER_CHB)

        self.joint_state = JointState(self.encoder, E_RPT)
        self.joint_state.estimate(state_estimate_hz=STATE_ESTIMATE_HZ, timer_no=1)

        self.timer = Timer(2)

    def publish_encoder_data(self, timer):
        theta = "{:.3f}".format(self.joint_state.theta)
        w = "{:.3f}".format(self.joint_state.w)
        msg = "ENC:" + str(self.encoder.ticks) + ":" + str(theta) + ":" + str(w)
        print(msg)

    def start(self):
        self.timer.init(period=50, mode=Timer.PERIODIC, callback=self.publish_encoder_data)
        while True:
            msg = input()
            try:
                msg_split = msg.split(':')
                if msg_split[0] == 'CMD':
                    cmd = float(msg_split[1])
                    self.motor.set_cmd(cmd)
            except:
                self.motor.set_cmd(0.0)
                print("Msg received with invalid structure!")
                self.dled.blink(20)
                break


def main():
    motor_encoder_assembly_test = MotorEncoderAssemblyTest()
    motor_encoder_assembly_test.start()
