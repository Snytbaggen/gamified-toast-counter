import sys
from pygame import USEREVENT

IS_RPI = sys.platform == "linux"

class Leds():
    TOTAL_LEDS = 32
    LEFT_LEDS = 16
    RIGHT_LEDS = 16

class Window():
    WIDTH = 800
    HEIGHT = 480
    FPS = 60

class Events():
    IO = USEREVENT + 0
    SYSTEM = USEREVENT + 100
    FLAPPY_TOAST = USEREVENT + 200