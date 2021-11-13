import math
from machine import Timer

class JointControl:
    def __init__(self, motor, js, kp, ki):
        self.motor = motor
        self.js = js
        self.kp = kp
        self.ki = ki

        self.target_w= 0 ## Public
        self.error_int = 0

        self.error_int_min = -1/self.ki
        self.error_int_max = 1/self.ki

    def update(self, dt): ## Public
        error = self.target_w - self.js.w
        cmd = (self.kp * error) + (self.ki * self.error_int)
        self.motor.set_cmd(cmd)
        self.update_error_int(error, dt)

    def update_error_int(self, error, dt):
        if self.target_w == 0:
            self.error_int = 0
            return
        error_int = self.error_int + (error * dt)
        if error_int < self.error_int_max and error_int > self.error_int_min:
            self.error_int = error_int

    def update_cb(self, timer):
        self.update(self.dt)

    def control(self, control_hz=100.0, timer_no=0):
        self.dt = 1/control_hz
        dt_milli = math.trunc(1000 * self.dt)
        self.timer = Timer(timer_no)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.update_cb)

