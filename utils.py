import pygame

def loadAndScale(resource, convert_alpha = False):
    return pygame.transform.scale2x(loadSprite(resource, convert_alpha))

def loadSprite(resource, convert_alpha = False):
    surface = pygame.transform.rotate(pygame.image.load(resource), 90)
    return surface.convert_alpha() if convert_alpha else surface.convert()

def loadSound(path):
    return pygame.mixer.Sound(path)

def blit(screen: pygame.Surface, resource, pos: tuple):
    screen.blit(resource, (pos[0], pos[1]))

def rotate(resource):
    return pygame.transform.rotate(resource, 90)