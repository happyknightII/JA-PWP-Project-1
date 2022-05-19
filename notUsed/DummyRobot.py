# Dummy version of Robot for testing purposes]
from notUsed.DummyLight import LightStrip


class Robot:
    def __init__(self, left_pins=None, right_pins=None):
        self.strip = LightStrip()

    def enable(self, thing=None):
        return

    def drive_raw(self, forward, turn):
        return

    def drive_time(self, power, duration):
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
