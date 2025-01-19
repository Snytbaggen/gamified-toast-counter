import pygame
from utils import *
from common import *
from toasterio import IOEvents, mockNfc

is_pressed = False

window_height = Window.HEIGHT + 148

font = pygame.font.Font('fonts/04B_19.TTF', 40)
btn_led = loadSprite("sprites/mock_btn_led.png", True)
btn_center = (window_height / 2, Window.WIDTH + 100)
btn_led_coord = (btn_center[0]-75, btn_center[1]-75)
btn_rect = btn_led.get_rect(center=btn_center)

nfc_one_center = (window_height / 4, Window.WIDTH + 100)
nfc_one_surf = font.render("NFC 1", True, (255, 255, 255))
nfc_one_rect = nfc_one_surf.get_rect(center=nfc_one_center)

nfc_two_center = (3 * window_height / 4, Window.WIDTH + 100)
nfc_two_surf = font.render("NFC 2", True, (255, 255, 255))
nfc_two_rect = nfc_two_surf.get_rect(center=nfc_two_center)

def draw(screen, brightness):
    pygame.draw.circle(screen, pygame.Color(0, 0, 200), btn_center, 75.0)
    btn_led.set_alpha(brightness)
    screen.blit(btn_led, btn_led_coord)
    screen.blit(nfc_one_surf, nfc_one_rect)
    screen.blit(nfc_two_surf, nfc_two_rect)

def check_press(events: list[pygame.event.Event]):
    global is_pressed
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if pygame.Rect.collidepoint(btn_rect, pos):
                if not is_pressed:
                    pygame.event.post(pygame.event.Event(IOEvents.EVENT_BUTTON_PRESS))
                    is_pressed = True
            elif pygame.Rect.collidepoint(nfc_one_rect, pos):
                mockNfc("0477ff04695f6181d6480000e1103e00")
            elif pygame.Rect.collidepoint(nfc_two_rect, pos):
                mockNfc("047369965b6f6180d5480000e1103e00")
        elif event.type == pygame.MOUSEBUTTONUP:
            if is_pressed:
                is_pressed = False
