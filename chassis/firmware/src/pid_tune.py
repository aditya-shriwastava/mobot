import math
from machine import Timer

from libs.motor import Motor
from libs.encoder import QuadratureEncoder
from libs.led import Led
from libs.joint_state import JointState
from libs.joint_control import JointControl

DLED = 2

M_CHA = 13
M_CHB = 12

E_TPR = 490
E_RPT = (1/E_TPR) * (2 * math.pi)
E_CHA = 25
E_CHB = 33

KP = 0.057
KI = 0.374
CONTROL_HZ = 100.0

STATE_ESTIMATE_HZ = 10

class PidTune:
    def __init__(self):
        self.dled = Led(DLED)
        self.motor = Motor(M_CHA, M_CHB)
        self.encoder = QuadratureEncoder(E_CHA, E_CHB, E_RPT)

        self.joint_state = JointState(self.encoder)
        self.joint_state.estimate(state_estimate_hz=STATE_ESTIMATE_HZ, timer_no=1)

        self.joint_control = JointControl(self.motor, self.joint_state, KP, KI)
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
                    self.joint_control.target_w = w
            except:
                self.motor.set_cmd(0.0)
                print("Msg received with invalid structure!")
                self.dled.blink(20)
                break

def main():
    pid_tune = PidTune()
    pid_tune.start()
