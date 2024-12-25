import pygame, sys
from constants import *

if IS_RPI:
    # I don't use Linux except on the Rpi, so this check is enough in my case
    from RPi import GPIO
else:
    import Mock.GPIO as GPIO

class IOEvents():
    EVENT_BUTTON_PRESS = pygame.USEREVENT + 1

BUTTON_PIN = 37

button_state = False if IS_RPI else True

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_button():
    global button_state
    new_state = not GPIO.input(BUTTON_PIN) # Active low, so we invert it
    if button_state != new_state:
        button_state = new_state
        if button_state:
            pygame.event.post(pygame.event.Event(IOEvents.EVENT_BUTTON_PRESS))
    
