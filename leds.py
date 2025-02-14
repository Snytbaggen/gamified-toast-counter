from typing import List
from toasterio import *
from common import Leds

class BtnLedController():
    def __init__(self):
        self.clear()
    
    def clear(self):
        self.brightness = 0
        self.counter = 1
        self.brightnessBuffer = [0]
        self.repetitions = 0
        self.shift_in = True
        self.step_delay = 1

    def set_data(self,
                 brightnessBuffer: List[int],
                 repetitions = 0,
                 shift_in = True,
                 step_delay = 1
                 ):
        self.brightnessBuffer = brightnessBuffer
        self.repetitions = repetitions
        self.shift_in = shift_in
        self.step_delay = step_delay
        self.move_led()

    def move_led(self):
        self.brightnessBuffer = self.brightnessBuffer[-1:] + self.brightnessBuffer[:-1]
        self.brightness = self.brightnessBuffer[0]
    
    def draw(self):
        self.counter -=1
        if self.counter <= 0:
            draw_btn_led(self.brightness)
            self.move_led()
            self.counter = self.step_delay

class LedController():
    def __init__(self):
        self.clear()

    def clear(self):
        self.leftBuffer = [Color(0, 0, 0)] * Leds.LEFT_LEDS
        self.rightBuffer = [Color(0, 0, 0)] * Leds.RIGHT_LEDS
        self.brightness = [0] * Leds.LEFT_LEDS
        self.counter = 1
        self.left = self.leftBuffer
        self.right = self.rightBuffer
        self.repetitions = 0
        self.shift_in = True
        self.step_delay = 1

    def set_data(self,
                left: List[Color],
                right: List[Color],
                brightness: List[int],
                repetitions = 0,
                shift_in = True,
                step_delay = 1
                ):
        self.left = left
        self.right = right
        self.brightness = brightness
        self.repetitions = repetitions
        self.shift_in = shift_in
        self.step_delay = step_delay
        self.move_leds()
    
    def move_leds(self):
        rotation = 1 if self.shift_in else Leds.LEFT_LEDS
        self.left = self.left[-rotation:] + self.left[:-rotation]
        self.right = self.right[-rotation:] + self.right[:-rotation]
        self.brightness = self.brightness[-1:] + self.brightness[:-1]

        self.leftBuffer = self.left[0:Leds.LEFT_LEDS]
        self.rightBuffer = self.right[0:Leds.RIGHT_LEDS]

    def draw(self):
        self.counter -= 1
        if self.counter <= 0:
            draw_leds(self.leftBuffer + self.rightBuffer, self.brightness[0])
            self.move_leds()
            self.counter = self.step_delay

shared_led_controller = LedController()
shared_btn_led_controller = BtnLedController()