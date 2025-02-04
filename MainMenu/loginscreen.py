import pygame
import toasterio as io
import users
from gamescreen import GameScreen
from utils import *
from common import *

class LoginScreen(GameScreen):
    def destination(self):
        return NavigationDestination.LOGIN
    
    def __init__(self):
        io.enable_nfc()
        self.btn_audio = loadSound("./audio/click.wav")

        self.bg = loadSprite("./sprites/scr_login.png")

        self.nfc_sound = loadSound("./audio/nfc_1.wav")

        self.btn_back = loadSprite("./sprites/btn_back.png", True)
        btn_back_pos = (705, (Window.HEIGHT / 2))
        self.btn_back_rect = self.btn_back.get_rect(center = btn_back_pos)
    
    def tick(self, screen, events):
        screen.blit(self.bg, (0, 0))

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                if checkPointCollision(self.btn_back_rect, pos):
                    self.btn_audio.play()
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
            if e.type == io.IOEvents.EVENT_NFC_READ:
                self.nfc_sound.play()
                id = e.dict["id"]

                pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
                
                if users.login_user(id):
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.USER}))
                elif not users.id_exists(id):
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.NEW_USER, "args": {"user_id": id}}))

        
        screen.blit(self.btn_back, self.btn_back_rect)
    
    def teardown(self):
        io.disable_nfc()
