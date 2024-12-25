import sys
from pygame import USEREVENT

IS_RPI = sys.platform == "linux"

class Window():
    WIDTH = 800
    HEIGHT = 480
    FPS = 60

class Events():
    IO = USEREVENT + 0
    SYSTEM = USEREVENT + 100
    FLAPPY_TOAST = USEREVENT + 200