#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

from .palette import Colors
from enum import Enum
import pygame


class ScreenType(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    QUIT = 3
    ERROR = 4
    SCORE = 5
    SCOREBOARD = 6
    COUNTDOWN = 7


class Screen:
    def __init__(self, game):
        self.game = game
        self.bg_color = Colors.DARK_BLUE1
        self.buttons = []
        self.background_colour = Colors.DARK_BLUE1
        self.hl_index = 0

    def draw(self):
        self.game.win.fill(self.background_colour)

    def show_text(self, string, x=0, y=0, color=Colors.GREEN, size=50):
        font = pygame.font.Font(self.game.current_font, size)
        text = font.render(string, True, color)
        textRect = text.get_rect()
        textRect.center = x, y
        self.game.win.blit(text, textRect)

    def process_event(self, event):
        raise NotImplementedError

    def quit_game(self):
        self.game.quit_game()
