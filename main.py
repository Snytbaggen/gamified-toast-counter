import pygame, sys
import toasterio as io
from constants import *
from FlappyToast.flappytoast import FlappyToastScreen
from MainMenu.startscreen import StartScreen

pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=1024)
print("Initializing pygame")
pygame.init()

if IS_RPI:
    screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT), pygame.FULLSCREEN, vsync=1)
else:
    outer = pygame.display.set_mode((Window.HEIGHT, Window.WIDTH), vsync=1)
    screen = pygame.Surface((Window.WIDTH, Window.HEIGHT))
    
clock = pygame.time.Clock()

start = StartScreen()
bird = FlappyToastScreen()

io.init()
start.init()
bird.init()

activeScreen = bird

while True:
    io.read_button()
    io.rainbow()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            io.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            activeScreen = bird

    activeScreen.tick(screen, events)
    if not IS_RPI:
        outer.blit(pygame.transform.rotate(screen, -90), (0, 0))
    pygame.display.update()
    clock.tick(Window.FPS)