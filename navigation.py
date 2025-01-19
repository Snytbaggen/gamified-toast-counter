from common import NavigationDestination
from gamescreen import GameScreen
from MainMenu import startscreen, userscreen, extrascreen, settingsscreen
from FlappyToast import flappytoast

stack = []

def init():
    stack.append(startscreen.StartScreen())

def current() -> GameScreen:
    return stack[-1]

def navigate(dest: NavigationDestination, args):
    global stack
    if current().destination == dest:
        return

    match dest:
        case NavigationDestination.BACK:
            if len(stack) > 1:
                stack.pop()
        case NavigationDestination.HOME:
            stack = stack[:1]
        case NavigationDestination.USER:
            stack.append(userscreen.UserScreen())
        case NavigationDestination.NEW_USER:
            stack.append(userscreen.NewUserScreen(args))
        case NavigationDestination.GAMES:
            stack.append(flappytoast.FlappyToastScreen())
        case NavigationDestination.EXTRA:
            stack.append(extrascreen.ExtraScreen())
        case NavigationDestination.SETTINGS:
            stack.append(settingsscreen.SettingsScreen())
