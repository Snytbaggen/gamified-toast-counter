import pygame
from gamescreen import GameScreenInterface
from utils import *
from constants import Window
from toasterio import IOEvents, Color
from leds import shared_led_controller

class StartScreen(GameScreenInterface):
    def init(self):
        self.font = pygame.font.Font('./gillies.ttf', 240)
        self.number = 0
        self.bg = loadSprite("./sprites/menu_bg.png")
        self.btn_audio = loadSound("./audio/btn_3.wav")
        self.leds = [Color(0, 130, 202)] * 16
        self.led_counter = 0

    def tick(self, screen, events):
        if (self.led_counter > 0):
            self.led_counter -= 1
        else:
            shared_led_controller.clear()
        for e in events:
            if e.type == IOEvents.EVENT_BUTTON_PRESS:
                self.number += 1
                self.led_counter = 20
                self.btn_audio.play()
                shared_led_controller.set_data(self.leds, self.leds, [50], 1, True, 10)
        
        screen.blit(self.bg, (0, 0))
        text = rotate(self.font.render(str(self.number), True, (255,255,255)))
        text_rect = text.get_rect(center=(Window.WIDTH / 2, Window.HEIGHT / 2))
        screen.blit(text, text_rect)