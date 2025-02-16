import pygame
from utils import *
from gamescreen import GameScreen
from toasterio import IOEvents, Color
from common import NavigationDestination
from leds import shared_led_controller, shared_btn_led_controller

class ExtraScreen(GameScreen):
    def destination(self):
        return NavigationDestination.EXTRA

    def __init__(self):
        self.click_audio = loadSound("./audio/click.wav")
        self.btn_audio = loadSound("./audio/btn_4.wav")

        self.bg = loadSprite("./sprites/scr_extra.png")

        self.btn_back = loadSprite("sprites/btn_back.png", True)
        btn_back_pos = (705, Window.HEIGHT / 2)
        self.btn_back_rect = self.btn_back.get_rect(center=btn_back_pos)

        leds = [Color(0, 130, 202)] * 16
        for i in range(len(leds)):
            leds[i] = colorWheel(i * (255 / 16))
        btn_led = [255, 0]

        shared_led_controller.set_data(leds, leds, [50], 1, True, 1)
        shared_btn_led_controller.set_data(btn_led, step_delay=20)

        self.audio_loop = loadSound("./audio/caramell_loop.wav")
        self.audio_loop.play(-1)

    def teardown(self):
        self.audio_loop.stop()

    def tick(self, screen, events):
        
        # Check events
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                if checkPointCollision(self.btn_back_rect, pos):
                    self.click_audio.play()
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
            if e.type == IOEvents.EVENT_BUTTON_PRESS:
                self.led_counter = 20
                self.btn_audio.play()
                

        # Draw to screen
        screen.blit(self.bg, (0, 0))
        screen.blit(self.btn_back, self.btn_back_rect)

    