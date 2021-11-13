from machine import Pin, PWM
import math

class Motor:
    '''
    cha and chb is such when cha is high and chb is low moter will rotate
    in counter-clockwise direction (i.e. +ve direction)
    '''
    def __init__(self, cha_pin_no, chb_pin_no, PWM_MAX=1023, PWM_HZ=2000):
        self.cha = PWM(Pin(cha_pin_no), freq=PWM_HZ, duty=0)
        self.chb = PWM(Pin(chb_pin_no), freq=PWM_HZ, duty=0)

        self.PWM_MAX = PWM_MAX

    '''
    -1.0 <= cmd <= 1.0
    Clockwise at Full Speed ---> Counter Clockwise at Full Speed
    '''
    def set_cmd(self, cmd): ## Public
        cmd_a = abs(max(0.0, cmd))
        cmd_b = abs(min(0.0, cmd))
        pwm_a = self.get_pwm_from_cmd(cmd_a)
        pwm_b = self.get_pwm_from_cmd(cmd_b)
        self.cha.duty(pwm_a)
        self.chb.duty(pwm_b)

    def get_pwm_from_cmd(self, cmd):
        pwm = math.trunc(cmd * self.PWM_MAX)
        if pwm > self.PWM_MAX:
            pwm = self.PWM_MAX
        elif pwm < 0:
            pwm = 0
        return pwm
