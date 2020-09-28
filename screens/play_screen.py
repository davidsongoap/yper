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
import sys
sys.path.append("..")
from util import fetch_words
from word import Word
from datetime import datetime
import pygame
import time


class PlayScreen(Screen):

    def __init__(self, game):
        super().__init__(game)
        self.started = False
        self.words = []
        self.typed_text = ""
        self.start_time = None
        self.correct_key_count = 0
        self.wpm = 0
        self.accuracy = 0
        self.hl_index = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:

            # start the timer when the first key is pressed
            if self.hl_index == 0:
                self.start_time = int(time.time())

            char = event.unicode.lower()
            word_completed, valid_char = self.words[self.hl_index].process_char(char)

            # the character typed was correct
            if valid_char:
                self.typed_text += char
                self.correct_key_count += 1
            else:
                self.correct_key_count -= 1

            if word_completed:
                # reset typed text
                self.typed_text = ""
                self.words[self.hl_index].toggle_active()
                self.hl_index += 1

                if self.hl_index == len(self.words):
                    # game ended
                    self.started = False
                    self.game.current_screen = ScreenType.MENU

                    # metrics
                    ending_time = int(time.time())
                    total_time = ending_time - self.start_time
                    self.game.recent_wpm = int((len(self.words) / total_time) * 60)
                    self.game.recent_accuracy = round((self.correct_key_count / self.total_keys) * 100,1)

                    self.correct_key_count = 0

                    # add to scoreboard
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    self.game.add_score((self.game.recent_wpm, self.game.recent_accuracy, dt_string))

                    self.game.current_screen = ScreenType.SCORE
                else:
                    # highlight next word
                    self.words[self.hl_index].toggle_active()

    def draw(self):
        super().draw()
        if not self.started:
            # when this screen opens the word list is generated
            self.generate_word_list()
            self.started = True

        # show words
        for word in self.words:
            word.draw()

        # show input
        self.display_input()

    def display_input(self):
        # input rectangles
        pygame.draw.rect(self.game.win, Colors.WHITE2,
                ((self.game.width//2)-235,515,450,70), border_radius=20)

        pygame.draw.rect(self.game.win, Colors.DARK_BLUE1,
                ((self.game.width//2)-230,520,440,60), border_radius=20)

        # show typed text
        self.show_text(self.typed_text, self.game.width//2, 550, Colors.WHITE1, 35)

        # icon
        self.show_text("", 280, 550, Colors.WHITE3, 65)

    def generate_word_list(self):
        # reset highlighted word position
        self.hl_index = 0

        # reset word list
        self.words = []

        # reset total key count
        self.total_keys = 0

        # fetch options for the word list
        n_paragraphs = 3
        min_words = 15
        max_words = 15

        word_list = fetch_words(n_paragraphs, min_words, max_words)

        last_pos = None  # position of the last word added to the list
        line_idx = 0
        line_padd = 55  # padding between each line
        word_padd = 20  # padding between each word
        left_side_padd = 35  # screen left side padding
        right_side_padd = 10  # screen right side padding
        top_padd = 20  # screen top side padding

        # creates Word instances and defines their position on the screen
        for word_txt in word_list:
            self.total_keys += len(word_txt)

            # word position
            x = last_pos[0] + word_padd if last_pos else left_side_padd
            y = (line_idx * line_padd) + top_padd

            new_word = Word(word_txt, x, y, self.game.current_font, self.game.win)

            # the word is out of the screen, go to next line
            if new_word.get_topright()[0] > self.game.width - right_side_padd:
                line_idx += 1
                new_word.change_pos(left_side_padd, (line_idx*line_padd)+top_padd)

            # save the last position
            last_pos = new_word.get_topright()

            self.words.append(new_word)

        # highlight the first word
        self.words[self.hl_index].toggle_active()

