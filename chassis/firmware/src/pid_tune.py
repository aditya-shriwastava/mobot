import math
from machine import Timer

from libs.motor import Motor
from libs.encoder import MonoDirEncoder
from libs.led import Led
from libs.joint_state import JointState
from libs.joint_control import JointControl
from mobot_data import *

motor = "Right"
if motor == "Right":
    M_CHA = MR_CHA
    M_CHB = MR_CHB
    MIN_OP = MIN_OPR
    E_CHA = ER_CHA
    E_CHB = ER_CHB
    KP = KPR
    KI = KIR
    W_MIN = WR_MIN
    W_MAX = WR_MAX
    GAMMA = GAMMA_R
elif motor == "Left":
    M_CHA = ML_CHA
    M_CHB = ML_CHB
    MIN_OP = MIN_OPL
    E_CHA = EL_CHA
    E_CHB = EL_CHB
    KP = KPL
    KI = KIL
    W_MIN = WL_MIN
    W_MAX = WL_MAX
    GAMMA = GAMMA_L

class PidTune:
    def __init__(self):
        self.dled = Led(DLED)
        self.motor = Motor(M_CHA, M_CHB, MIN_OP)
        self.encoder = MonoDirEncoder(E_CHA, E_CHB)

        self.joint_state = JointState(self.encoder, E_RPT)
        self.joint_state.estimate(state_estimate_hz=STATE_ESTIMATE_HZ, timer_no=1)

        self.joint_control = JointControl(self.motor, self.joint_state, KP, KI, W_MIN, W_MAX, GAMMA)
        self.joint_control.control(control_hz=CONTROL_HZ, timer_no=2)

        self.publish_w_timer = Timer(3)

    def publish_w(self, timer):
        w = "{:.2f}".format(self.joint_state.w)
        msg = "W:" + str(w)
        print(msg)

    def start(self):
        self.publish_w_timer.init(period=100, mode=Timer.PERIODIC, callback=self.publish_w)
        while True:
            msg = input()
            try:
                msg_split = msg.split(':')
                if msg_split[0] == 'PCMD':
                    if msg_split[1] == 'GET':
                        p = "{:.3f}".format(self.joint_control.kp)
                        msg = "P:" + str(p)
                        print(msg)
                    else:
                        p = float(msg_split[1])
                        self.joint_control.kp = p
                elif msg_split[0] == 'ICMD':
                    if msg_split[1] == 'GET':
                        i = "{:.3f}".format(self.joint_control.ki)
                        msg = "I:" + str(i)
                        print(msg)
                    else:
                        i = float(msg_split[1])
                        self.joint_control.ki = i
                elif msg_split[0] == 'WCMD':
                    w = float(msg_split[1])
                    self.joint_control.set_target_w(w)
            except:
                self.motor.set_cmd(0.0)
                print("Msg received with invalid structure!")
                self.dled.blink(20)
                break

def main():
    pid_tune = PidTune()
    pid_tune.start()
