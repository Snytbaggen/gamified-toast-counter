from common import NavigationDestination
from gamescreen import GameScreen
from MainMenu import startscreen
from FlappyToast import flappytoast

stack = []

def init():
    stack.append(startscreen.StartScreen())

def current() -> GameScreen:
    return stack[-1]

def navigate(dest: NavigationDestination):
    global stack
    match dest:
        case NavigationDestination.BACK:
            if len(stack) > 1:
                stack.pop()
        case NavigationDestination.HOME:
            stack = stack[:1]
        case NavigationDestination.GAMES:
            stack.append(flappytoast.FlappyToastScreen())
