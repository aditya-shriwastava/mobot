from machine import Pin, Timer
import math

class Led:
    def __init__(self, pin_no, timer_no=0):
        self.pin = Pin(pin_no, Pin.OUT)
        self.pin.off()
        self.timer = Timer(timer_no)

    def on(self): ## Public
        self.timer.deinit()
        self.pin.on()

    def off(self): ## Public
        self.timer.deinit()
        self.pin.off()

    def blink(self, hz): ## Public
        self.timer.deinit()
        dt_milli = math.trunc(1000/hz)
        self.timer.init(period=dt_milli, mode=Timer.PERIODIC, callback=self.toggle)

    def toggle(self, timer):
        if self.pin.value() == 0:
            self.pin.on()
        else:
            self.pin.off()
