import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 72        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


class LightStrip(PixelStrip):
    def __init__(self, brightness=LED_BRIGHTNESS):
        super(LightStrip, self).__init__(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, brightness, LED_CHANNEL)
        self.begin()

    # Define functions which animate LEDs in various ways.
    def color_wipe(self, rgb, wait_ms=50, show=True):

        """Wipe color across display a pixel at a time."""
        for i in range(self.numPixels()):
            self.setPixelColor(i, Color(rgb[0], rgb[1], rgb[2]))
            if show:
                self.show()
            time.sleep(wait_ms / 1000.0)

    def theater_chase(self, rgb, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, Color(rgb[0], rgb[1], rgb[2]))
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, 0)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.numPixels()):
                self.setPixelColor(i, wheel((i + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * iterations):
            for i in range(self.numPixels()):
                self.setPixelColor(i, wheel(
                    (int(i * 256 / self.numPixels()) + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    def theater_chase_rainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, wheel((i + j) % 255))
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.numPixels(), 3):
                    self.setPixelColor(i + q, 0)

    def set_pixel(self, index, rgb):
        self.setPixelColor(index, Color(rgb[0], rgb[1], rgb[2]))

    def turn_off(self, show=True):
        self.color_wipe((0, 0, 0), 0)
        self.show()

    def __del__(self):
        self.turn_off()
