#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

import pygame
import time

from .screen import Screen, ScreenType
from .palette import Colors


class CountdownScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.started = False
        self.count_number = 3
        self.last_time_stamp = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_screen = ScreenType.MENU

    def draw(self):
        super().draw()
        self.show_text(str(self.count_number),
                       self.game.width//2,
                       self.game.height//2,
                       size=100, color=Colors.LIGHT_BLUE1)
        if not self.started:
            self.started = True
            self.last_time_stamp =time.time()
        else:
            curr_time = time.time()
            if curr_time - self.last_time_stamp >= 1:
                self.count_number -= 1
                self.last_time_stamp = curr_time
            if self.count_number == 0:
                self.started = False
                self.count_number = 3
                self.game.current_screen = ScreenType.GAME

