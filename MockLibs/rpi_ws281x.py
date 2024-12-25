class Adafruit_NeoPixel(object):
    def __init__(self, leds, pins, freq, dma, invert, brightness, channel):
        self.leds = leds

    def begin(self):
        pass

    def setPixelColor(self, index, color):
        pass

    def show(self):
        pass

    def numPixels(self):
        return self.leds

class Color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b