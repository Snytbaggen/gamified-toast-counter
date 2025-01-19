import pygame
from common import *

class Adafruit_NeoPixel(object):
    def __init__(self, leds, pins, freq, dma, invert, brightness, channel):
        self.leds = leds
        self.brightness = brightness
        self.colors = [Color(0, 0, 0)] * leds

    def begin(self):
        pass

    def setBrightness(self, brigthness):
        self.brightness = brigthness

    def setPixelColor(self, index, color):
        self.colors[index] = color

    def show(self):
        pass

    def numPixels(self):
        return self.leds

    # Used for mocking LEDs when running on a non-Pi
    def draw(self, screen):
        led_s = pygame.Surface((42, 42))
        led_s.set_alpha((self.brightness * 20) & 255)
        for i in range(Leds.LEFT_LEDS + Leds.RIGHT_LEDS):
            led_s.fill(self.colors[i].toPygame())
            if (i >= Leds.LEFT_LEDS):
                ycoord = 4 + ((i - Leds.LEFT_LEDS) * 50)
                xcoord = 90 + Window.HEIGHT
            else:
                ycoord = 4 + (i * 50)
                xcoord = 16
            pygame.draw.rect(screen, (0, 0, 0), (xcoord, ycoord, 42, 42))
            screen.blit(led_s, (xcoord, ycoord))

class Color():
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def toPygame(self):
        return pygame.Color(self.r, self.g, self.b)