from enum import Enum
from pygame import USEREVENT

class Window():
    WIDTH = 480
    HEIGHT = 800
    FPS = 60

class Events():
    IO = USEREVENT + 0
    SYSTEM = USEREVENT + 100
    FLAPPY_TOAST = USEREVENT + 200