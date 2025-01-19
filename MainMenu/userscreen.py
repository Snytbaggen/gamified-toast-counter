import pygame
import users
from keyboard import Keyboard
from gamescreen import GameScreen
from utils import *
from common import Window, NavigationDestination
from toasterio import IOEvents, Color
from leds import shared_led_controller, shared_btn_led_controller

class NewUserScreen(GameScreen):
    def destination(self):
        return NavigationDestination.NEW_USER
    
    def __init__(self, args):
        if not "user_id" in args:
            pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
        else:
            self.user_id = args["user_id"]

        self.click_audio = loadSound("./audio/click.wav")

        self.username_input = ""
        self.username_font = pygame.font.Font('fonts/baloo.ttf', 40)
        self.username_pos = (290, Window.HEIGHT / 2)

        self.message_font = pygame.font.Font('fonts/baloo.ttf', 32)
        self.message_pos_upper = (582, Window.HEIGHT / 2)
        self.message_pos_lower = (622, Window.HEIGHT / 2)

        self.in_error_state = False

        self.bg = loadSprite("./sprites/scr_new_user.png")
        self.keyboard = Keyboard()

        self.btn_cancel = loadSprite("sprites/btn_cancel.png", True)
        btn_cancel_pos = (705, (Window.HEIGHT / 2) - 105)
        self.btn_cancel_rect = self.btn_cancel.get_rect(center=btn_cancel_pos)

        self.btn_ok = loadSprite("sprites/btn_ok.png", True)
        btn_ok_pos = (705, (Window.HEIGHT / 2) + 105)
        self.btn_ok_rect = self.btn_ok.get_rect(center=btn_ok_pos)
    
    def tick(self, screen, events):
        screen.blit(self.bg, (0, 0))

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                char = self.keyboard.check_press(pos)
                if char == "↑":
                    self.click_audio.play()
                    self.keyboard.shift_pressed = not self.keyboard.shift_pressed
                elif char == "←":
                    self.click_audio.play()
                    if len(self.username_input) > 0:
                        self.username_input = self.username_input[:-1]
                elif char != None:
                    self.click_audio.play()
                    if len(self.username_input) < 15:
                        self.username_input += char
                        self.keyboard.shift_pressed = False
                elif checkPointCollision(self.btn_cancel_rect, pos):
                    self.click_audio.play()
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
                elif checkPointCollision(self.btn_ok_rect, pos):
                    self.click_audio.play()
                    if len(self.username_input) > 0:
                        if users.name_exists(self.username_input):
                            self.in_error_state = True
                        else:
                            users.create_user(self.user_id, self.username_input)
                            pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
                            pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.USER}))


        username_text_surf = rotate(self.username_font.render(self.username_input, True, (0, 130,202)))
        username_text_rect = username_text_surf.get_rect(center=self.username_pos)
        screen.blit(username_text_surf, username_text_rect)

        message_text_upper = "Välj nåt coolt!" if not self.in_error_state else "Namnet används redan!"
        message_text_upper_surf = rotate(self.message_font.render(message_text_upper, True, (255,255,255)))
        message_text_upper_rect = message_text_upper_surf.get_rect(center=self.message_pos_upper)
        screen.blit(message_text_upper_surf, message_text_upper_rect)

        message_text_lower = "Max 15 tecken." if not self.in_error_state else "Välj ett nytt."
        message_text_lower_surf = rotate(self.message_font.render(message_text_lower, True, (255,255,255)))
        message_text_lower_rect = message_text_lower_surf.get_rect(center=self.message_pos_lower)
        screen.blit(message_text_lower_surf, message_text_lower_rect)

        screen.blit(self.btn_ok, self.btn_ok_rect)
        screen.blit(self.btn_cancel, self.btn_cancel_rect)

        self.keyboard.draw(screen)

class UserScreen(GameScreen):
    def destination(self):
        return NavigationDestination.USER
    
    def __init__(self):
        self.click_audio = loadSound("./audio/click.wav")

        self.number_font = pygame.font.Font('fonts/gillies.ttf', 240)
        self.number_pos = (352, Window.HEIGHT / 2)

        self.text_font = pygame.font.Font('fonts/baloo.ttf', 40)
        self.text_pos = (243, Window.HEIGHT / 2)

        self.btn_back = loadSprite("sprites/btn_logout.png", True)
        btn_back_pos = (581, Window.HEIGHT / 2)
        self.btn_back_rect = self.btn_back.get_rect(center=btn_back_pos)

        self.bg = loadSprite("./sprites/scr_toastcounter.png")
        self.btn_audio = loadSound("./audio/btn_4.wav")
        self.leds = [Color(0, 130, 202)] * 16
        self.btn_led = [255]
        self.led_counter = 0

    def tick(self, screen, events):
        if (self.led_counter > 0):
            self.led_counter -= 1
        else:
            shared_led_controller.clear()
            shared_btn_led_controller.clear()
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                if checkPointCollision(self.btn_back_rect, pos):
                    self.click_audio.play()
                    users.logout()
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
            if e.type == IOEvents.EVENT_BUTTON_PRESS:
                users.increment_toast()
                self.led_counter = 20
                self.btn_audio.play()
                shared_led_controller.set_data(self.leds, self.leds, [50], 1, True, 1)
                shared_btn_led_controller.set_data(self.btn_led)
        
        screen.blit(self.bg, (0, 0))

        if users.current_user != None:
            number = rotate(self.number_font.render(str(users.current_user["toasts"]), True, (255,255,255)))
            number_rect = number.get_rect(center=self.number_pos)
            screen.blit(number, number_rect)

            text = rotate(self.text_font.render(users.current_user["name"], True, (255,255,255)))
            text_rect = text.get_rect(center=self.text_pos)
            screen.blit(text, text_rect)

        screen.blit(self.btn_back, self.btn_back_rect)
