import pygame, sys
from constants import *

if IS_RPI:
    # I don't use Linux except on the Rpi, so this check is enough in my case
    from RPi import GPIO
    from rpi_ws281x import *
else:
    import Mock.GPIO as GPIO
    from MockLibs.rpi_ws281x import *

class IOEvents():
    EVENT_BUTTON_PRESS = pygame.USEREVENT + 1

BUTTON_PIN = 37

LED_COUNT = 40
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 5
LED_INVERT = False
LED_CHANNEL = 0

button_state = False if IS_RPI else True

def init():
    global leds
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    leds.begin()

def quit():
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))
    leds.show()

def read_button():
    global button_state
    new_state = not GPIO.input(BUTTON_PIN) # Active low, so we invert it
    if button_state != new_state:
        button_state = new_state
        if button_state:
            pygame.event.post(pygame.event.Event(IOEvents.EVENT_BUTTON_PRESS))


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

def rainbow():
    global leds
    """Draw rainbow that fades across all pixels at once."""
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0,0,255))
    leds.show()
    
