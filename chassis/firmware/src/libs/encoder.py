from machine import Pin

class Encoder:
    def __init__(self, ROTATION_PER_TICK):
        self.ROTATION_PER_TICK = ROTATION_PER_TICK
        self.theta = 0 ## Public
        self.ticks = 0 ## Public

class MonoEncoder(Encoder):
    def __init__(self, pin, ROTATION_PER_TICK):
        super().__init__(ROTATION_PER_TICK)
        self.pin = Pin(pin, Pin.IN)
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.on_state_change)

    def on_state_change(self, pin):
        if self.pin == pin:
            self.theta += self.ROTATION_PER_TICK
            self.ticks += 1

class QuadratureEncoder(Encoder):
    def __init__(self, cha_pin, chb_pin, ROTATION_PER_TICK):
        super().__init__(ROTATION_PER_TICK)
        self.cha_pin = Pin(cha_pin, Pin.IN)
        self.chb_pin = Pin(chb_pin, Pin.IN)
        self.cha_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.on_state_change)
        self.chb_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.on_state_change)

    def on_state_change(self, pin):
        if pin == self.cha_pin:
            if self.cha_pin.value() == self.chb_pin.value():
                self.theta += self.ROTATION_PER_TICK
                self.ticks += 1
            else:
                self.theta -= self.ROTATION_PER_TICK
                self.ticks -= 1
        elif pin == self.chb_pin:
            if self.cha_pin.value() == self.chb_pin.value():
                self.theta -= self.ROTATION_PER_TICK
                self.ticks -= 1
            else:
                self.theta += self.ROTATION_PER_TICK
                self.ticks += 1
