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

def drawOutline(
        screen: pygame.Surface,
        textCenter,
        font: pygame.font.Font,
        text, fontColor, borderColor, borderThickness):
    
    outlineSurf = rotate(font.render(text, True, borderColor))
    outlineSize = outlineSurf.get_size()

    textSurf = pygame.Surface((outlineSize[0] + 2*borderThickness, outlineSize[1] + 2*borderThickness), pygame.SRCALPHA)
    textRect = textSurf.get_rect()

    offsets = [(ox, oy)
               for ox in range(-borderThickness, 2*borderThickness, borderThickness)
               for oy in range(-borderThickness, 2*borderThickness, borderThickness)
               if ox != 0 or oy != 0]
    for ox, oy in offsets:
        px, py = textRect.center
        textSurf.blit(outlineSurf, outlineSurf.get_rect(center = (px+ox, py+oy)))

    innerText = rotate(font.render(text, True, fontColor))

    textSurf.blit(innerText, innerText.get_rect(center = textRect.center))
    textRect.center = textCenter
    screen.blit(textSurf, textRect)
