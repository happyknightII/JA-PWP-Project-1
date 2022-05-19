from Motor import Motor, clean_up
from time import time, sleep
from Light import LightStrip

LEFT_PINS = (14, 15, 24)
RIGHT_PINS = (17, 27, 23)
x = 0.4
y = -1.3


class Robot:
    def __init__(self, left_pins=LEFT_PINS, right_pins=RIGHT_PINS):
        self.motors = (Motor((left_pins[0], left_pins[1]), left_pins[2]),
                       Motor((right_pins[0], right_pins[1]), right_pins[2]))
        self.strip = LightStrip()

    def enable(self, thing=True):
        self.motors[0].enable(thing)
        self.motors[1].enable(thing)

    def stop(self):
        self.motors[0].set_power(0)
        self.motors[1].set_power(0)

    def drive_raw(self, forward, turn):
        left = forward - turn
        right = forward - turn
        if abs(left) > 2:
            self.motors[0].set_power(left)
        else:
            self.motors[0].set_power(0)

        if abs(right) > 2:
            self.motors[1].set_power(right)
        else:
            self.motors[1].set_power(0)

    def drive_time(self, power, duration):
        self.enable()
        start_time = time()
        delta_time = 0
        while delta_time < duration:
            self.motors[0].set_power(power[0])
            self.motors[1].set_power(power[1])
            delta_time = time() - start_time
        self.motors[0].set_power(0)
        self.motors[1].set_power(0)

    def forward(self, sec):
        if sec > 0:
            self.drive_time((74.46 + x, 68.2 + y), sec)
        elif sec < 0:
            self.drive_time((-64, -68.2), -sec)

    def turn(self, degrees):
        if degrees > 0:
            self.drive_time((45 + x, 0), 1.33 * degrees / 90)
        elif degrees < 0:
            self.drive_time((0, 43.74 + y), 1.33 * -degrees / 90)

    def auto(self):
        self.drive_time((74.46 + x, 68.2 + y), 2.97)
        sleep(1)
        self.drive_time((50 + x, 0), 1.33)
        sleep(1)
        self.drive_time((74.46 + x, 68.2 + y), 3.5)
        sleep(1)
        self.drive_time((-64, -68.2), 1.3)
        sleep(1)
        self.drive_time((50 + x, 0), 1.33)
        sleep(1)
        self.drive_time((74.46 + x, 68.2 + y), 3)

    def indicate(self):
        for i in range(23, 45):
            self.strip.set_pixel(i, (100, 100, 100))

        self.strip.show()

    def __del__(self):
        del self.motors
        clean_up()
