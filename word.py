#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

import pygame

from palette import Colors


class Word:
    def __init__(self, text, x, y, font, win):
        self.text = text
        self.x = x
        self.y = y
        self.win = win
        self.active = False
        self.error = False
        self.font = pygame.font.Font(font, 35)
        self.text_render = self.font.render(self.text, True, Colors.DARK_BLUE1)
        self.textRect = self.text_render.get_rect()
        self.textRect.topleft = (self.x, self.y)
        self.current_char_idx = 0

    def toggle_active(self):
        self.active = not self.active

    def get_topleft(self):
        return self.textRect.topleft

    def get_topright(self):
        return self.textRect.topright

    def change_pos(self, x, y):
        self.textRect.topleft = (x, y)

    def draw(self):
        background_color = Colors.WHITE1 if self.active else Colors.DARK_BLUE2
        if self.error and self.active:
            background_color = Colors.RED
        horizontal_padding = 5
        button_width = (self.textRect.topright[0]-self.textRect.topleft[0]) + horizontal_padding*2

        button_height = self.textRect.bottomright[1] - self.textRect.topright[1]

        button_background_pos = (self.textRect.topleft[0]-horizontal_padding,
                                 self.textRect.topleft[1],
                                 button_width,
                                 button_height)
        radius = 8
        pygame.draw.rect(self.win, background_color,
                         button_background_pos, border_radius=radius)

        self.win.blit(self.text_render, self.textRect)

    def change_color(self, color):
        self.text_render = self.font.render(self.text, True, color)

    def process_char(self,char):
        valid_char = False
        if char == self.text[self.current_char_idx]:
            self.current_char_idx+=1
            self.error = False
            valid_char = True
        else:
            self.error = True

        word_finished = self.current_char_idx == len(self.text)

        return self.current_char_idx == len(self.text), valid_char
