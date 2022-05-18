from Motor import Motor, cleanUp
from time import time, sleep
from Light import LightStrip

LEFT_PINS = (14, 15, 24)
RIGHT_PINS = (17, 27, 23)
x = 0.4
y = -1.3


class Robot:
    def __init__(self, leftPins=LEFT_PINS, rightPins=RIGHT_PINS):
        self.motors = (Motor((leftPins[0], leftPins[1]), leftPins[2]), Motor((rightPins[0], rightPins[1]), rightPins[2]))
        self.strip = LightStrip()

    def enable(self, thing=True):
        self.motors[0].enable(thing)
        self.motors[1].enable(thing)

    def driveRaw(self, forward, turn):
        left = forward - turn
        right = forward - turn
        if abs(left) > 0.1:
            self.motors[0].setPower(left)
        else:
            self.motors[0].setPower(0)
        if abs(right) > 0.1:
            self.motors[1].setPower(right)
        else:
            self.motors[1].setPower(0)

    def driveTime(self, power, duration):
        self.enable()
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
            self.driveTime((74.46 + x, 68.2 + y), sec)
        elif sec < 0:
            self.driveTime((-64, -68.2), -sec)

    def turn(self, degrees):
        if degrees > 0:
            self.driveTime((45 + x, 0), 1.33 * degrees / 90)
        elif degrees < 0:
            self.driveTime((0, 43.74 + y), 1.33 * -degrees / 90)

    def auto(self):
        self.driveTime((74.46 + x, 68.2 + y), 2.97)
        sleep(1)
        self.driveTime((50 + x, 0), 1.33)
        sleep(1)
        self.driveTime((74.46 + x, 68.2 + y), 3.5)
        sleep(1)
        self.driveTime((-64, -68.2), 1.3)
        sleep(1)
        self.driveTime((50 + x, 0), 1.33)
        sleep(1)
        self.driveTime((74.46 + x, 68.2 + y), 3)

    def indicate(self):
        for i in range(23, 45):
            self.strip.setPixel(i, (100, 100, 100))

        self.strip.show()

    def __del__(self):
        del self.motors
        cleanUp()
