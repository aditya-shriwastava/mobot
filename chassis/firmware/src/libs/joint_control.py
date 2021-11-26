import math
from machine import Timer

def is_within(x, eps):
    if x < eps and x > -eps:
        return True
    else:
        return False

class JointControl:
    def __init__(self, motor, js, kp, ki, target_w_min, target_w_max, gamma):
        self.motor = motor
        self.js = js
        self.kp = kp
        self.ki = ki

        self.target_w= 0
        self.error_int = 0

        self.target_w_min = target_w_min
        self.target_w_max = target_w_max
        self.gamma = gamma

        self.error_int_max = 1/self.ki

    def set_target_w(self, w): ## Public
        if is_within(w, self.target_w_max):
            self.target_w = w
            # if is_within(w, self.target_w_min):
            #     self.target_w = 0
        else:
            self.target_w = (w / abs(w)) * self.target_w_max

    def update(self, dt): ## Public
        error = self.target_w - self.js.w
        cmd = (self.kp * error) + (self.ki * self.error_int)
        self.motor.set_cmd(cmd)
        self.update_error_int(error, dt)

    def update_error_int(self, error, dt):
        if self.target_w == 0:
            self.error_int = 0
            return
        if is_within(self.error_int , self.error_int_max):
            gamma = 1
            if is_within(self.error_int , self.error_int_max * self.motor.min_op):
                gamma = self.gamma
        else:
            gamma = 0
        self.error_int += gamma * error * dt

    def update_cb(self, timer):
        self.update(self.dt)

    def control(self, control_hz=100.0, timer_no=0): ## Public
        self.dt = 1/control_hz
        dt_milli = math.trunc(1000 * self.dt)
        self.timer = Timer(timer_no)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.update_cb)

