import pygame
from utils import *
from constants import *
from toasterio import IOEvents

is_pressed = False

def init():
    global btn_led, btn_center, btn_led_coord, btn_rect
    btn_led = loadSprite("sprites/mock_btn_led.png", True)
    btn_center = ((Window.HEIGHT / 2) + 74, Window.WIDTH + 100)
    btn_led_coord = (btn_center[0]-75, btn_center[1]-75)
    btn_rect = btn_led.get_rect(center=btn_center)

def draw(screen, brightness):
    global btn_led, btn_center, btn_led_coord
    pygame.draw.circle(screen, pygame.Color(0, 0, 200), btn_center, 75.0)
    btn_led.set_alpha(brightness)
    screen.blit(btn_led, btn_led_coord)

def check_press(events: list[pygame.event.Event]):
    global is_pressed, btn_led, btn_rect
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if pygame.Rect.collidepoint(btn_rect, pos):
                if not is_pressed:
                    pygame.event.post(pygame.event.Event(IOEvents.EVENT_BUTTON_PRESS))
                    is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if is_pressed:
                is_pressed = False
