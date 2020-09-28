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

class MenuScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.hl_index = 0
        self.init_buttons()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.toggle_buttons((self.hl_index - 1))
            if event.key == pygame.K_DOWN:
                self.toggle_buttons((self.hl_index + 1))
            if event.key == pygame.K_RETURN:
                self.buttons[self.hl_index].execute()

    def toggle_buttons(self, new_index):
        new_index = new_index % len(self.buttons)
        self.buttons[self.hl_index].toggle_highlight()
        self.buttons[new_index].toggle_highlight()
        self.hl_index = new_index

    def init_buttons(self):

        # Main menu buttons
        self.buttons.append(Button(self.game, "Play",
                                   self.game.width//2, 320,
                                   ScreenType.GAME, size=65))

        self.buttons.append(Button(self.game, "Options",
                                   self.game.width//2, 403,
                                   ScreenType.OPTIONS, size=50))

        self.buttons.append(Button(self.game, "Scoreboard",
                                   self.game.width//2, 475,
                                   ScreenType.SCOREBOARD, size=50))

        self.buttons.append(Button(self.game, "Quit",
                                   self.game.width//2, 545,
                                   ScreenType.QUIT, size=45, bg_color=Colors.RED))

        # Play button starts highlighted
        self.buttons[self.hl_index].toggle_highlight()

    def draw(self):
        super().draw()
        #  show title
        self.show_text("YPER", size=210, color=Colors.LIGHT_BLUE1,
                       x=self.game.width//2, y=150)

        pygame.draw.rect(self.game.win, self.background_colour,(490,85,100,45))
        #  show buttons
        for b in self.buttons:
            b.draw()

