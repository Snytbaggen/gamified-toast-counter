import pygame
from gamescreen import GameScreenInterface
from utils import *
from constants import Window
from toasterio import IOEvents, Color
from leds import shared_led_controller, shared_btn_led_controller

class Icon():
    def __init__(self, path, center, destination = None):
        self.surface = loadSprite(path, True)
        self.rect = self.surface.get_rect(center=center)
    
    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.surface, self.rect)
    
    def check_press(self, pos):
        if checkPointCollision(self.rect, pos):
            print("Click detected")

class StartScreen(GameScreenInterface):
    def init(self):
        self.font = pygame.font.Font('fonts/gillies.ttf', 240)
        self.number = 0
        self.bg = loadSprite("./sprites/menu_home.png")
        self.btn_audio = loadSound("./audio/btn_4.wav")
        self.leds = [Color(0, 130, 202)] * 16
        self.btn_led = [255]
        self.led_counter = 0
        self.text_pos = (220, Window.HEIGHT / 2)
        self.icons = [
            Icon("sprites/ic_settings.png", (656, (Window.HEIGHT / 2) - 122)),
            Icon("sprites/ic_star.png", (656, Window.HEIGHT / 2)),
            Icon("sprites/ic_controller.png", (656, (Window.HEIGHT / 2) + 122))
        ]

    def tick(self, screen, events):
        if (self.led_counter > 0):
            self.led_counter -= 1
        else:
            shared_led_controller.clear()
            shared_btn_led_controller.clear()
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                for ic in self.icons:
                    ic.check_press(pos)
            if e.type == IOEvents.EVENT_BUTTON_PRESS:
                self.number += 1
                self.led_counter = 20
                self.btn_audio.play()
                shared_led_controller.set_data(self.leds, self.leds, [50], 1, True, 1)
                shared_btn_led_controller.set_data(self.btn_led)
        
        screen.blit(self.bg, (0, 0))

        text = rotate(self.font.render(str(self.number), True, (255,255,255)))
        text_rect = text.get_rect(center=self.text_pos)
        screen.blit(text, text_rect)
        for ic in self.icons:
            ic.draw(screen)
