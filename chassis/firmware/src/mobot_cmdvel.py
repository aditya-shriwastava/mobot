from libs.motor import Motor
from libs.encoder import MonoDirEncoder
from libs.led import Led
from libs.joint_state import JointState
from libs.joint_control import JointControl
from libs.diff_drive_state_estimator import DiffDriveStateEstimator
from libs.diff_drive_controller import DiffDriveController

from mobot_data import *

class Mobot:
    def __init__(self):
        self.mr = Motor(MR_CHA, MR_CHB, MIN_OPR)
        self.ml = Motor(ML_CHA, ML_CHB, MIN_OPL)
        self.er = MonoDirEncoder(ER_CHA, ER_CHB)
        self.el = MonoDirEncoder(EL_CHA, EL_CHB)
        self.dled = Led(DLED)

        self.js_r = JointState(self.er, E_RPT)
        self.js_l = JointState(self.el, E_RPT)

        self.jc_r = JointControl(self.mr, self.js_r, KPR, KIR, W_MIN, W_MAX, GAMMA_R)
        self.jc_l = JointControl(self.ml, self.js_l, KPL, KIL, W_MIN, W_MAX, GAMMA_L)

        self.diff_drive_state_estimator = DiffDriveStateEstimator(self.js_r, self.js_l, L, D,\
                                          state_estimate_hz=STATE_ESTIMATE_HZ,\
                                          timer_no=1)
        self.diff_drive_controller = DiffDriveController(self.jc_r, self.jc_l, L, D,\
                                     control_hz=CONTROL_HZ,\
                                     timer_no=2)

def main():
    mobot = Mobot()
    while True:
        msg = input()
        try:
            msg_split = msg.split(':')
            if msg_split[0] == "CMDVEL":
                data = msg_split[1].split(',')
                wr = float(data[0])
                wl = float(data[1])
                mobot.jc_r.set_target_w(wr)
                mobot.jc_l.set_target_w(wl)
            elif msg_split[0] == "GET":
                if msg_split[1] == "Metadata":
                    metadata_msg = "Metadata:" + str(D) + ","\
                                               + str(L) + ","\
                                               + str(W_MAX) + ","\
                                               + str(W_MIN)
                    print(metadata_msg)
        except:
            print("Msg received with invalid structure!")
            mobot.dled.blink(20)
            break

if __name__ == "__main__":
    main()
