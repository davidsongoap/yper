#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

import pygame
from screens import GameScreen, ScreenType

pygame.init()


class Game:
    def __init__(self):
        self.width = 950
        self.height = 630
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((self.width, self.height))
        icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption('YPER')
        self.running = True
        self.current_font = "fonts/Fira Code.ttf"
        self.current_screen = ScreenType.MENU
        self.screen = GameScreen(self)
        self.accuracy = 0
        self.wpm = 0

    def get_font(self):
        return self.current_font

    def change_screen(self, new_screen):
        self.current_screen = new_screen

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # the screen processess the pygame events
            self.screen.process_event(event)

    def run(self):
        # main app loop
        while self.running:
            self.clock.tick(self.FPS)
            self.process_events()
            self.draw()
        pygame.quit()

    def draw(self):
        self.screen.draw()
        pygame.display.update()


game = Game()
game.run()
