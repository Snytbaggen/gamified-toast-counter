import pygame, sys
import toasterio as io
from constants import *
from FlappyToast.flappytoast import FlappyToastScreen
from MainMenu.startscreen import StartScreen
from leds import shared_led_controller

pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=1024)
print("Initializing pygame")
pygame.init()

if IS_RPI:
    screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT), pygame.FULLSCREEN, vsync=1)
else:
    outer = pygame.display.set_mode((Window.HEIGHT + 148, Window.WIDTH), vsync=1)
    screen = pygame.Surface((Window.WIDTH, Window.HEIGHT))
    
clock = pygame.time.Clock()

start = StartScreen()
bird = FlappyToastScreen()

io.init()
start.init()
bird.init()

activeScreen = bird

leds = [io.Color(0, 130, 202), io.Color(5, 82, 144)] * 8
shared_led_controller.set_data(leds, leds, [50, 50], 0, True, 60)

while True:
    io.read_button()
    io.check_nfc()
    shared_led_controller.draw()
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
        outer.blit(pygame.transform.rotate(screen, -90), (74, 0))
        io.mockLeds(outer)
    pygame.display.update()
    clock.tick(Window.FPS)