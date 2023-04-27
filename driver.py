import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

class Motor:
    def __init__(self, pin, lowerLimit, upperLimit, lowerValLimit, upperValLimit, offSet=0,  invert=False):
        gpio.setup(pin, gpio.OUT)
        self.motor = gpio.PWM(pin, 50)
        self.motor.start(0)

        self.offSet = offSet
        self.inverted = invert
        self.pin = pin
        self.ll = lowerLimit
        self.ul = upperLimit
        self.lvl = lowerValLimit
        self.uvl = upperValLimit

    def set(self, val):
        ret = val
        if self.inverted:
            half = (self.uvl - self.lvl)/2 + self.lvl
            val = half-val+half
        if self.lvl<=val<=self.uvl:
            scale = 100/(self.ul-self.ll)
            duty = (((val/scale)+(self.ll+self.ul)/2)+self.offSet)/10+2
            gpio.output(self.pin, gpio.HIGH)
            self.motor.ChangeDutyCycle(duty)
        return ret

    def setPower(self, val):
        if 0<=val<=100:
            gpio.output(self.pin, gpio.HIGH)
            self.motor.ChangeDutyCycle(val)


class DriveMotor:
    def __init__(self, forward, reverse, forwardLimit, reverseLimit,):
        self.forward = forward
        self.reverse = reverse
        self.forwardLimit = forwardLimit
        self.reverseLimit = reverseLimit

    def set(self, val):
        if self.reverseLimit<=val<=self.forwardLimit:
            if val < 0:
                self.forward.setPower(0)
                self.reverse.setPower(-val)
            else:
                self.reverse.setPower(0)
                self.forward.setPower(val)

steerMotor = Motor(12, 35, 65, -50, 50, 3)
forward = Motor(32, 0, 100, 0, 100)
reverse = Motor(35, 0, 100, 0, 100)
driveMotor = DriveMotor(forward, reverse, 100, -100)
angles = [0,50,0,-50]

def steer(angle):
    steerMotor.set(angle)

def speed(spe):
    driveMotor.set(spe)

