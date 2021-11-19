import math
from machine import Timer

class DiffDriveController:
    def __init__(self, jc_r, jc_l, L, D,  timer_no=0, control_hz=100):
        self.dt = 1/control_hz
        dt_milli = math.trunc(1000 * self.dt)
        self.jc_r = jc_r
        self.jc_l = jc_l

        self.L = L
        self.D = D

        self.timer = Timer(timer_no)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.update_cb)

    def set_target_velocity(self, v, w): ## Public
        wr = -(1/(self.D/2)) * (v + (w * (self.L/2)))
        wl = (1/(self.D/2)) * (v - (w * (self.L/2)))
        self.jc_r.set_target_w(wr)
        self.jc_l.set_target_w(wl)

    def update_cb(self, timer):
        self.jc_r.update(self.dt)
        self.jc_l.update(self.dt)
