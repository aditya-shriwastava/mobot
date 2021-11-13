import math
from machine import Timer

from libs.joint_state import JointState

class DiffDriveStateEstimator:
    def __init__(self, er, el, L, D, timer_no=0, state_estimate_hz=10):
        self.dt = 1/state_estimate_hz
        dt_milli = math.trunc(1000 * self.dt)

        self.js_r = JointState(er) ## Public
        self.js_l = JointState(el) ## Public

        self.timer = Timer(timer_no)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.update_cb)

        self.D = D
        self.L = L

        self.v = 0.0 ## Public
        self.w = 0.0 ## Public

    def update_cb(self, timer):
        self.js_r.update(self.dt)
        self.js_l.update(self.dt)

        self.v = (self.js_l.w - self.js_r.w) * (self.D/4)
        self.w = -(self.js_r.w + self.js_l.w) * (self.D/(2 * self.L))
