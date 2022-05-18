# Dummy version of light for testing purposes

class LightStrip:
    def __init__(self, brightness=None):
        return

    def set_pixel_color(self):
        return

    def show(self):
        return

    def color_wipe(self, rgb, wait_ms=None, show=None):
        return

    def theater_chase(self, rgb, wait_ms=None, iterations=None):
        return

    def rainbow(self, wait_ms=None, iterations=None):
        return

    def rainbow_cycle(self, wait_ms=None, iterations=None):
        return

    def theater_chase_rainbow(self, wait_ms=None):
        return

    def set_pixel(self, index, rgb):
        return

    def turn_off(self, show=None):
        return

    def __del__(self):
        self.turn_off()
