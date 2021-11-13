from libs.motor import Motor
from libs.encoder import MonoEncoder
from libs.led import Led
from libs.diff_drive_state_estimator import DiffDriveStateEstimator
from libs.diff_drive_controller import DiffDriveController

from mobot_data import *

class Mobot:
    def __init__(self):
        self.mr = Motor(MR_CHA, MR_CHB)
        self.ml = Motor(ML_CHA, ML_CHB)
        self.er = MonoEncoder(ER, E_RPT)
        self.el = MonoEncoder(EL, E_RPT)
        self.dled = Led(DLED)

        self.diff_drive_state_estimator = DiffDriveStateEstimator(self.er, self.el, L, D,\
                                          state_estimate_hz=STATE_ESTIMATE_HZ,\
                                          timer_no=1)
        self.diff_drive_controller = DiffDriveController(self.mr, self.ml,\
                                     self.diff_drive_state_estimator,\
                                     KP, KI, L, D,\
                                     control_hz=CONTROL_HZ,\
                                     timer_no=2)

def main():
    mobot = Mobot()
    while True:
        msg = input()
        try:
            msg_split = msg.split(',')
            v = float(msg_split[0])
            w = float(msg_split[1])
        except:
            print("Msg received with invalid structure!")
            mobot.dled.blink(20)
            break
        mobot.diff_drive_controller.set_target_velocity(v, w)

if __name__ == "__main__":
    main()
