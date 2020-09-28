#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

from .screen import Screen, ScreenType
from .buttons import Button
from .palette import Colors
import pygame

class ScoreScreen(Screen):

    def __init__(self, game):
        super().__init__(game)
        self.init_buttons()

    def toggle_buttons(self, new_index):
        new_index = new_index % len(self.buttons)
        self.buttons[self.hl_index].toggle_highlight()
        self.buttons[new_index].toggle_highlight()
        self.hl_index = new_index

    def draw(self):
        super().draw()

        self.show_text("WPM", self.game.width//2, 120, Colors.WHITE1, 70)
        self.show_text(str(self.game.recent_wpm), self.game.width//2, 190, Colors.LIGHT_BLUE2, 80)

        self.show_text("Accuracy", self.game.width//2, 300, Colors.WHITE1, 60)
        self.show_text(str(self.game.recent_accuracy) + "%", self.game.width//2, 370, Colors.LIGHT_BLUE2, 80)

        for b in self.buttons:
            b.draw()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.toggle_buttons((self.hl_index - 1))
            if event.key == pygame.K_DOWN:
                self.toggle_buttons((self.hl_index + 1))
            if event.key == pygame.K_RETURN:
                self.buttons[self.hl_index].execute()

    def init_buttons(self):
        self.buttons.append(Button(self.game, "Play Again",
                                   self.game.width//2, (self.game.height//2) + 170,
                                   ScreenType.GAME, size=40, bg_color=Colors.WHITE1))
        self.buttons.append(Button(self.game, "Return to Menu",
                                   self.game.width//2, (self.game.height//2) + 240,
                                   ScreenType.MENU, size=40, bg_color=Colors.WHITE1))

        self.buttons[0].toggle_highlight()

