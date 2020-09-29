#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

from .screen import Screen


class QuitScreen(Screen):
    # Note: This screen is not supposed to show anything. It just closes the game
    def __init__(self, game):
        super().__init__(game)

    def draw(self):
        self.quit_game()

    def process_event(self, event):
        pass
