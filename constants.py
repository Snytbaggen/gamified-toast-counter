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
    PC_WIDTH = HEIGHT + (2 * 74) # Extra 74 px on each side
    PC_HEIGHT = WIDTH + 200 # Extra 200 px at the bottom

class Events():
    IO = USEREVENT + 0
    SYSTEM = USEREVENT + 100
    FLAPPY_TOAST = USEREVENT + 200