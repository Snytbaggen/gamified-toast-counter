import pygame
from utils import rotate, checkPointCollision
from common import Window

class Key():
    def __init__(self, character, center):
        self.surface = pygame.Surface((37, 37), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(center=center)
        self.center = center
        self.character = character
    
    def draw(self, screen, font):
        char_surf = rotate(font.render(self.character, True, (0,53,95)))
        char_rect = char_surf.get_rect(center=(20, 20))
        self.surface.fill((255,255,255))
        self.surface.blit(char_surf, char_rect)
        screen.blit(self.surface, self.surface_rect)
    
    def checkClick(self, pos):
        if checkPointCollision(self.surface_rect, pos):
            return self.character
        return None

class Keyboard():
    def __init__(self):
        self.font = pygame.font.Font("fonts/baloo.ttf", 24)
        lower_case_chars = "1234567890←qwertyuiopåasdfghjklöä↑zxcvbnm,.-"
        upper_case_chars = "!\"#¤%&/()=←QWERTYUIOPÅASDFGHJKLÖÄ↑ZXCVBNM;:_"

        self.lower_case_keys = []
        self.upper_case_keys = []
        
        offset = 40
        for row in range(4):
            for col in range(11):
                index = (row * 11) + col
                coord = (row*offset + 400, Window.HEIGHT - col*offset - 40)
                self.lower_case_keys.append(Key(lower_case_chars[index], coord))
                self.upper_case_keys.append(Key(upper_case_chars[index], coord))


    shift_pressed = False

    def draw(self, screen):
        for key in self.upper_case_keys if self.shift_pressed else self.lower_case_keys:
            key.draw(screen, self.font)
    
    def check_press(self, pos):
        for key in self.upper_case_keys if self.shift_pressed else self.lower_case_keys:
            char = key.checkClick(pos)
            if char != None:
                return char

