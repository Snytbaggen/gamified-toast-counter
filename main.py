import pygame, sys
import toasterio as io
from constants import *
from FlappyToast.flappytoast import FlappyToastScreen
from MainMenu.startscreen import StartScreen

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
print("Initializing pygame")
pygame.init()
outer = pygame.display.set_mode((Window.HEIGHT, Window.WIDTH), vsync=1)
screen = pygame.Surface((Window.WIDTH, Window.HEIGHT))
clock = pygame.time.Clock()

start = StartScreen()
bird = FlappyToastScreen()

io.init()
start.init()
bird.init()

activeScreen = start

while True:
    io.read_button()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            activeScreen = bird

    activeScreen.tick(screen, events)
    outer.blit(pygame.transform.rotate(screen, 90), (0, 0))
    pygame.display.update()
    clock.tick(Window.FPS)