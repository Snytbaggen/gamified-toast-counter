import pygame, sys
import toasterio as io
import navigation
import users
from common import *
from utils import *
from FlappyToast.flappytoast import FlappyToastScreen
from MainMenu.startscreen import StartScreen
from leds import shared_led_controller, shared_btn_led_controller

pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=1024)
pygame.init()

if IS_RPI:
    screen = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT), pygame.FULLSCREEN, vsync=1)
    pygame.mouse.set_visible(False)
else:
    outer = pygame.display.set_mode((Window.PC_WIDTH, Window.PC_HEIGHT), vsync=1)
    screen = pygame.Surface((Window.WIDTH, Window.HEIGHT))
    from MockLibs import mock_button
    
clock = pygame.time.Clock()

start = StartScreen()
bird = FlappyToastScreen()

io.init()
navigation.init()

nfc_sound = loadSound("./audio/nfc_1.wav")

while True:
    io.read_button()
    io.check_nfc()
    shared_led_controller.draw()
    shared_btn_led_controller.draw()
    events = pygame.event.get()
    for event in events:
        if event.type == io.IOEvents.EVENT_NFC_READ:
            current = navigation.current().destination()
            if current != NavigationDestination.USER and current != NavigationDestination.NEW_USER:
                nfc_sound.play()
                id = event.dict["id"]
                if users.login_user(id):
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.USER}))
                elif not users.id_exists(id):
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.NEW_USER, "args": {"user_id": id}}))
        elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            io.quit()
            sys.exit()
        elif event.type == SystemEvents.NAVIGATE:
            print(event.dict)
            dest = event.dict["dest"]
            args = event.dict["args"] if "args" in event.dict else {}
            if dest:
                navigation.navigate(dest, args)

    navigation.current().tick(screen, events)
    if not IS_RPI:
        outer.blit(pygame.transform.rotate(screen, -90), (74, 0))
        io.mockLeds(outer)
        mock_button.draw(outer, shared_btn_led_controller.brightness)
        mock_button.check_press(events)
    pygame.display.update()
    clock.tick(Window.FPS)