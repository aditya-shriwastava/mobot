import math
from machine import Timer

class JointState:
    def __init__(self, encoder, ROTATION_PER_TICK):
        self.ROTATION_PER_TICK = ROTATION_PER_TICK
        self.encoder = encoder
        self.w = 0.0 ## Public
        self.theta = 0.0 ## Public

    def update(self, dt): ## Public
        theta = self.encoder.ticks * self.ROTATION_PER_TICK
        self.w = (theta - self.theta) / dt
        self.theta = theta

    def update_cb(self, timer):
        self.update(self.dt)

    def estimate(self, state_estimate_hz=10.0, timer_no=0): ## Public
        self.dt = 1/state_estimate_hz
        dt_milli = math.trunc(1000 * self.dt)
        self.timer = Timer(timer_no)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.update_cb)

