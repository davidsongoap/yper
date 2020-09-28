#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

from .screen import Screen

class CountdownScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

    def process_event(self, event):
        pass

    def draw(self):
        super().draw()

