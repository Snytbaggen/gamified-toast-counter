import sys
import pygame
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
    PC_HEIGHT = WIDTH + 200 # Extra 200 px at the

class BaseEvents():
    IO = USEREVENT + 0
    SYSTEM = USEREVENT + 100
    FLAPPY_TOAST = USEREVENT + 200

class SystemEvents():
    NAVIGATE = BaseEvents.SYSTEM + 1

class NavigationDestination():
    BACK = 1
    HOME = 2
    SETTINGS = 3
    USER =  4
    NEW_USER = 5
    EXTRA = 6
    GAMES = 7
    LOGIN = 8
