from common import NavigationDestination
from typing import List
import pygame

class GameScreen:
    def destination(self) -> NavigationDestination:
        pass

    def tick(self, screen: pygame.Surface, events: List[pygame.event.Event]):
        pass