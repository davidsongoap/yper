#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

import pygame
from .palette import Colors


class Button():

    def __init__(self, game, text, x, y, new_screen, size=50, bg_color=Colors.WHITE1):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.new_screen = new_screen
        self.game = game
        self.highlighted = False
        self.bg_color = bg_color

    def draw(self):
        text_color = Colors.WHITE1 if not self.highlighted else Colors.DARK_BLUE1
        background_color = Colors.DARK_BLUE2 if not self.highlighted else self.bg_color

        font = pygame.font.Font(self.game.get_font(), self.size)
        text = font.render(self.text, True, text_color)
        textRect = text.get_rect()
        textRect.center = self.x, self.y

        side_padding = 20

        button_width = (textRect.topright[0]-textRect.topleft[0]) + side_padding*2

        button_height = textRect.bottomright[1] - textRect.topright[1]

        button_background_pos = (textRect.topleft[0]-side_padding,
                                 textRect.topleft[1], button_width, button_height)
        button_radius = 8
        pygame.draw.rect(self.game.win, background_color,
                         button_background_pos, border_radius=button_radius)

        self.game.win.blit(text, textRect)

    def toggle_highlight(self):
        self.highlighted = not self.highlighted

    def execute(self):
        self.game.change_screen(self.new_screen)


class OptionsButton(Button):
    pass
