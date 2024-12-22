import pygame, sys
import toasterio as io
from constants import *
from FlappyToast.flappytoast import FlappyToastScreen

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
print("Initializing pygame")
pygame.init()
screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT), vsync=1)
clock = pygame.time.Clock()

bird = FlappyToastScreen()

io.init()
bird.init()

activeScreen = bird

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    activeScreen.tick(screen, events)
    pygame.display.update()
    clock.tick(60)