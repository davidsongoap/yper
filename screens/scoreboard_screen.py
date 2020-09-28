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

class ScoreBoardScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

    def draw(self):
        super().draw()

        board_y_pos = 150
        self.show_text("SCOREBOARD", size=90, x=self.game.width/2, y=60, color=Colors.LIGHT_BLUE1)
        pygame.draw.rect(self.game.win,self.background_colour,(420,33,30,20))
        self.show_text("", size=25, x=600, y=board_y_pos-25, color=Colors.LIGHT_BLUE3)
        self.show_text("", size=30, x=220, y=board_y_pos-25, color=Colors.LIGHT_BLUE3)
        self.show_text("什", size=30, x=343, y=board_y_pos-25, color=Colors.LIGHT_BLUE3)
        line_gap = 45
        for i in range(10):
            if i == 0: color = Colors.DARK_BLUE4
            elif i == 1: color = Colors.DARK_BLUE3
            elif i == 2: color = Colors.DARK_BLUE3
            else: color = Colors.DARK_BLUE2
            pygame.draw.rect(self.game.win,color,(420,board_y_pos+(line_gap*i),370,30),border_radius=5)
            pygame.draw.rect(self.game.win,color,(170,board_y_pos+(line_gap*i),100,30),border_radius=5)
            pygame.draw.rect(self.game.win,color,(285,board_y_pos+(line_gap*i),120,30),border_radius=5)

        for j in range(len(self.game.scoreboard)):
            wpm = self.game.scoreboard[j][0]
            accuracy = self.game.scoreboard[j][1]
            date = self.game.scoreboard[j][2]
            self.show_text(str(wpm), size=26, x=220, y=board_y_pos+16+(line_gap*j), color=Colors.WHITE1)
            self.show_text(str(accuracy)+"%", size=26, x=345, y=board_y_pos + 16+(line_gap*j),color=Colors.WHITE1)
            self.show_text(str(date), size=26, x=605, y=board_y_pos + 16+(line_gap*j),color=Colors.WHITE1)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_screen = ScreenType.MENU
