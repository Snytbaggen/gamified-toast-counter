import pygame
from subprocess import call
from utils import *
from gamescreen import GameScreen
from common import NavigationDestination

class SettingsScreen(GameScreen):
    def destination(self):
        return NavigationDestination.SETTINGS

    def __init__(self):
        self.click_audio = loadSound("./audio/click.wav")

        self.bg = loadSprite("./sprites/scr_settings.png")

        self.btn_back = loadSprite("sprites/btn_back.png", True)
        btn_back_pos = (705, Window.HEIGHT / 2)
        self.btn_back_rect = self.btn_back.get_rect(center=btn_back_pos)

        self.btn_shutdown = loadSprite("sprites/btn_shutdown.png", True)
        btn_shutdown_pos = (Window.WIDTH / 2, Window.HEIGHT / 2)
        self.btn_shutdown_rect = self.btn_shutdown.get_rect(center=btn_shutdown_pos)

    def tick(self, screen, events):
        
        # Check events
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = e.pos
                if checkPointCollision(self.btn_back_rect, pos):
                    self.click_audio.play()
                    pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": NavigationDestination.BACK}))
                elif checkPointCollision(self.btn_shutdown_rect, pos):
                    self.click_audio.play()
                    if IS_RPI:
                        call("sudo shutdown -h now", shell=True)
                    else:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Draw to screen
        screen.blit(self.bg, (0, 0))
        screen.blit(self.btn_back, self.btn_back_rect)
        screen.blit(self.btn_shutdown, self.btn_shutdown_rect)



call("sudo poweroff", shell=True)