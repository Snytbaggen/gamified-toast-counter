import pygame
from gamescreen import GameScreenInterface
from constants import Window

class StartScreen(GameScreenInterface):
    def init(self):
        smallfont = pygame.font.SysFont('Corbel', 40)
        self.text = smallfont.render('Start', True, (255,255,255))
    
    def tick(self, screen, events):
        screen.blit(self.text, (20, 20))