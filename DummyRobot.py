# Dummy version of Robot for testing purposes]
from DummyLight import LightStrip


class Robot:
    def __init__(self, leftPins=None, rightPins=None):
        self.strip = LightStrip()

    def enable(self, thing=None):
        return

    def driveRaw(self, forward, turn):
        return

    def driveTime(self, power, duration):
        return

    def forward(self, sec):
        return

    def turn(self, degrees):
        return

    def auto(self):
        return

    def indicate(self):
        return

    def __del__(self):
        return
