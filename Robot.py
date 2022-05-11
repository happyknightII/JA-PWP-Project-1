from Motor import Motor
from time import time, sleep
# import math
from Light import LightStrip
import RPi.GPIO as IO

LEFT_PINS = (14, 15, 24)
RIGHT_PINS = (17, 27, 23)
x = 0.4
y = -1.3


class Robot:
    def __init__(self, leftPins=LEFT_PINS, rightPins=RIGHT_PINS):
        self.motors = (Motor((leftPins[0], leftPins[1]), leftPins[2]), Motor((rightPins[0], rightPins[1]), rightPins[2]))
        self.strip = LightStrip()

    def drive(self, power, duration):
        self.motors[0].enable()
        self.motors[1].enable()
        # start = 1.4
        startTime = time()
        deltaTime = 0
        while deltaTime < duration:
            self.motors[0].setPower(power[0])
            self.motors[1].setPower(power[1])
            deltaTime = time() - startTime
        self.motors[0].setPower(0)
        self.motors[1].setPower(0)

    def forward(self, sec):
        if sec > 0:
            self.drive((74.46+x, 68.2+y), sec)
        elif sec < 0:
            self.drive((-64, -68.2), -sec)

    def turn(self, degrees):
        if degrees > 0:
            self.drive((45+x, 0), 1.33 * degrees/90)
        elif degrees < 0:
            self.drive((0, 43.74+y), 1.33 * -degrees/90)

    def auto(self):
        self.drive((74.46+x, 68.2+y), 2.97)
        self.pause(1)
        self.drive((50+x, 0), 1.33)
        self.pause(1)
        self.drive((74.46+x, 68.2+y), 3.5)
        self.pause(1)
        self.drive((-64, -68.2), 1.3)
        self.pause(1)
        self.drive((50+x, 0), 1.33)
        self.pause(1)
        self.drive((74.46+x, 68.2+y), 3)

    def indicate(self, index):
        for i in range(72):
            if i < index:
                self.strip.setPixel(index, (int(i/index), int(i/index), int(i/index)))
            else:
                self.strip.setPixel(index, (int((index-i)/index), int((index-i)/index), int((index-i)/index)))
        self.strip.show()

    def pause(self, time1):
        sleep(time1)

    def __del__(self):
        del self.motors
        IO.cleanup()
