import pygame

def loadAndScale(resource, convert_alpha = False):
    return pygame.transform.scale2x(loadSprite(resource, convert_alpha))

def loadSprite(resource, convert_alpha = False):
    surface = pygame.image.load(resource)
    return surface.convert_alpha() if convert_alpha else surface.convert()

def loadSound(path):
    return pygame.mixer.Sound(path)