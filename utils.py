import pygame
from common import IS_RPI, Window, NavigationDestination, SystemEvents

class Icon():
    def __init__(self, path, center, destination: NavigationDestination = None):
        self.surface = loadSprite(path, True)
        self.rect = self.surface.get_rect(center=center)
        self.destination = destination
        self.click_audio = loadSound("./audio/click.wav")
    
    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.surface, self.rect)
    
    def check_press(self, pos):
        if checkPointCollision(self.rect, pos):
            self.click_audio.play()
            pygame.event.post(pygame.event.Event(SystemEvents.NAVIGATE, {"dest": self.destination}))

def checkPointCollision(rect, point) -> bool:
    if IS_RPI:
        return pygame.Rect.collidepoint(rect, point)
    else:
        # When running on a non-Pi the screen is both rotated and has extra padding added.
        # To account for this the point is flipped and the padding subtracted.
        offset = (Window.PC_WIDTH - Window.HEIGHT) / 2
        return pygame.Rect.collidepoint(rect, (point[1], Window.HEIGHT - point[0] + offset))

def loadAndScale(path, convert_alpha = False) -> pygame.surface.Surface:
    return pygame.transform.scale2x(loadSprite(path, convert_alpha))

def loadSprite(path, convert_alpha = False) -> pygame.surface.Surface:
    surface = pygame.transform.rotate(pygame.image.load(path), 90)
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
