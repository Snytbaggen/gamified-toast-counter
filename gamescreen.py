from typing import List
import pygame

class GameScreenInterface:
    def init(self):
        pass

    def tick(self, screen: pygame.Surface, events: List[pygame.event.Event]):
        pass