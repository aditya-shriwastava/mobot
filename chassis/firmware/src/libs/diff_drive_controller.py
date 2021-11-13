import math
from machine import Timer

from libs.joint_control import JointControl

class DiffDriveController:
    def __init__(self, mr, ml, diff_drive_state_estimator, kp, ki, L, D,  timer_no=0, control_hz=100):
        self.dt = 1/control_hz
        dt_milli = math.trunc(1000 * self.dt)
        self.jc_r = JointControl(mr, diff_drive_state_estimator.js_r, kp, ki)
        self.jc_l = JointControl(ml, diff_drive_state_estimator.js_l, kp, ki)

        self.L = L
        self.D = D

        self.timer = Timer(timer_no)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.update_cb)

    def set_target_wheel_velocity(self, wr, wl): ## Public
        self.jc_r.target_w = wr
        self.jc_l.target_w = wl

    def set_target_velocity(self, v, w): ## Public
        wr = -(1/(self.D/2)) * (v + (w * (self.L/2)))
        wl = (1/(self.D/2)) * (v - (w * (self.L/2)))
        self.jc_r.target_w = wr
        self.jc_l.target_w = wl

    def update_cb(self, timer):
        self.jc_r.update(self.dt)
        self.jc_l.update(self.dt)
