#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

from .screen import Screen, ScreenType
from .palette import Colors
import pygame

class OptionsScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_screen = ScreenType.MENU

    def draw(self):
        super().draw()
        self.show_text("", x=self.game.width//2,
                       y=(self.game.height//2) - 50, size=250, color=Colors.WHITE2)
        self.show_text("coming soon", x=self.game.width//2,
                       y=(self.game.height//2) + 130, size=60, color=Colors.WHITE2)

