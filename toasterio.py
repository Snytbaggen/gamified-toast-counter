import pygame, sys
from typing import List
from constants import *

if IS_RPI:
    # I don't use Linux except on the Rpi, so this check is enough in my case
    from RPi import GPIO
    from rpi_ws281x import *
    from mfrc522 import MFRC522
else:
    import Mock.GPIO as GPIO
    from MockLibs.rpi_ws281x import *
    from MockLibs.MFRC522 import MFRC522

class IOEvents():
    EVENT_BUTTON_PRESS = pygame.USEREVENT + 1
    EVENT_NFC_READ = pygame.USEREVENT + 2

BUTTON_PIN = 37
BUTTON_LED_PIN = 33

LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 5
LED_INVERT = False
LED_CHANNEL = 0

button_state = False if IS_RPI else True
nfc = MFRC522()

def init():
    global leds, btn_led
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_LED_PIN, GPIO.OUT)
    btn_led = GPIO.PWM(33, 1000)
    btn_led.start(0)
    leds = Adafruit_NeoPixel(Leds.TOTAL_LEDS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    leds.begin()

def quit():
    for i in range(leds.numPixels()):
        leds.setPixelColor(i, Color(0, 0, 0))
    leds.show()

def read_button():
    global button_state
    new_state = not GPIO.input(BUTTON_PIN) # Active low, so we invert it
    if button_state != new_state:
        button_state = new_state
        if button_state:
            pygame.event.post(pygame.event.Event(IOEvents.EVENT_BUTTON_PRESS))

def check_nfc():
    global nfc
    status, _ = nfc.MFRC522_Request(nfc.PICC_REQIDL)
    if status != nfc.MI_OK:
        return
    status, _ = nfc.MFRC522_Anticoll()
    buf = nfc.MFRC511_Read(0)
    nfc.MFRC522_Request(nfc.PICC_HALT)
    if buf:
        id = ''.join([format(x, "02x") for x in buf])
        pygame.event.post(pygame.event.Event(IOEvents.EVENT_NFC_READ, { "id": id }))


def draw_leds(colors: List[Color], brightness):
    global leds
    leds.setBrightness(brightness)
    for i in range(Leds.TOTAL_LEDS):
        leds.setPixelColor(i, colors[i])
    leds.show()

def draw_btn_led(brightness):
    btn_led.ChangeDutyCycle((brightness * 100) / 255)
    pass

def mockLeds(screen):
    global leds
    leds.draw(screen)

def mockNfc(id):
    global nfc
    nfc.SetMockId(id)
