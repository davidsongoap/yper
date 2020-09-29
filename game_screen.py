#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

from screens import *
from util import check_internet


class GameScreen:
    # This class is used to manage the screens

    def __init__(self, game):
        self.game = game
        self.screens = None
        self.init_screens()

        # check internet connection
        if not check_internet():
            self.game.current_screen = ScreenType.ERROR

    def process_event(self, event):
        # pygame.event is processed by the current screen
        self.screens[self.game.current_screen.value].process_event(event)

    def init_screens(self):
        # Instantiates all of the screens
        #
        # Note: The index of each screen on this list should always
        # match it's corresponding value on the ScreenType Enum
        self.screens = [MenuScreen(self.game),
                        PlayScreen(self.game),
                        OptionsScreen(self.game),
                        QuitScreen(self.game),
                        ErrorScreen(self.game),
                        ScoreScreen(self.game),
                        ScoreBoardScreen(self.game),
                        CountdownScreen(self.game)]

    def draw(self):
        # draw the current screen
        self.screens[self.game.current_screen.value].draw()
