import pygame, sys
from typing import List
from constants import *

if IS_RPI:
    # I don't use Linux except on the Rpi, so this check is enough in my case
    from RPi import GPIO
    from rpi_ws281x import *
    import MFRC522
else:
    import Mock.GPIO as GPIO
    from MockLibs.rpi_ws281x import *
    from MockLibs.MFRC522 import MFRC522

class IOEvents():
    EVENT_BUTTON_PRESS = pygame.USEREVENT + 1

BUTTON_PIN = 37

LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 5
LED_INVERT = False
LED_CHANNEL = 0

button_state = False if IS_RPI else True
nfc = MFRC522()

def init():
    global leds
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    leds = Adafruit_NeoPixel(Leds.TOTAL_LEDS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
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

def check_nfc():
    pass

def draw_leds(colors: List[Color], brightness):
    global leds
    leds.setBrightness(brightness)
    for i in range(Leds.TOTAL_LEDS):
        leds.setPixelColor(i, colors[i])
    leds.show()

def mockLeds(screen):
    global leds
    leds.draw(screen)
    
