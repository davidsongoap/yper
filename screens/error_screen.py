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

class ErrorScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.init_buttons()

    def init_buttons(self):
        self.buttons.append(Button(self.game, "Exit",
                                   self.game.width//2, (self.game.height//2) + 200,
                                   ScreenType.QUIT, size=55, bg_color=Colors.RED))

        self.buttons[0].toggle_highlight()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.current_screen = ScreenType.QUIT

    def draw(self):
        super().draw()
        self.show_text("睊", x=self.game.width//2,
                       y=(self.game.height//2)-100, size=300, color=Colors.RED)

        self.show_text("No Internet Connection!", x=self.game.width//2,
                       y=(self.game.height//2) + 100, size=30, color=Colors.WHITE1)
        for b in self.buttons:
            b.draw()
