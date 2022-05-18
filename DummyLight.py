# Dummy version of light for testing purposes

class LightStrip:
    def __init__(self, brightness=None):
        return

    def setPixelColor(self):
        return

    def show(self):
        return

    def colorWipe(self, rgb, wait_ms=None, show=None):
        return

    def theaterChase(self, rgb, wait_ms=None, iterations=None):
        return

    def rainbow(self, wait_ms=None, iterations=None):
        return

    def rainbowCycle(self, wait_ms=None, iterations=None):
        return

    def theaterChaseRainbow(self, wait_ms=None):
        return

    def setPixel(self, index, rgb):
        return

    def turnOff(self, show=None):
        return

    def __del__(self):
        self.turnOff()
