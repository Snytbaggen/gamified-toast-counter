import pygame
import users
from gamescreen import GameScreen
from utils import *
from common import Window, NavigationDestination
from toasterio import IOEvents, Color
from leds import shared_led_controller, shared_btn_led_controller

class StartScreen(GameScreen):
    def destination(self):
        return NavigationDestination.HOME

    def __init__(self):
        self.font = pygame.font.Font('fonts/gillies.ttf', 240)
        self.bg = loadSprite("./sprites/menu_home.png")
        self.btn_audio = loadSound("./audio/btn_2.wav")
        self.leds = [Color(255, 0, 0)] * 16
        self.btn_led = [255]
        self.led_counter = 0
        self.text_pos = (220, Window.HEIGHT / 2)
        self.icons = [
            Icon("sprites/ic_settings.png", (656, (Window.HEIGHT / 2) - 122), NavigationDestination.SETTINGS),
            Icon("sprites/ic_star.png", (656, Window.HEIGHT / 2), NavigationDestination.EXTRA),
            Icon("sprites/ic_controller.png", (656, (Window.HEIGHT / 2) + 122), NavigationDestination.GAMES)
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
                self.led_counter = 20
                self.btn_audio.play()
                shared_led_controller.set_data(self.leds, self.leds, [50], 1, True, 1)
                shared_btn_led_controller.set_data(self.btn_led)
        
        screen.blit(self.bg, (0, 0))

        text = rotate(self.font.render(str(users.total_toast), True, (255,255,255)))
        text_rect = text.get_rect(center=self.text_pos)
        screen.blit(text, text_rect)
        for ic in self.icons:
            ic.draw(screen)
