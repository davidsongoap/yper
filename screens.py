#  __  __ ____   ______ ____
#  \ \/ // __ \ / ____// __ \
#   \  // /_/ // __/  / /_/ /
#   / // ____// /___ / _, _/
#  /_//_/    /_____//_/ |_|
#
#  By Davidson Gonçalves
#  github.com/davidsongoap/yper

import pygame
from enum import Enum
from palette import Colors
from util import fetch, check_internet
from word import Word
from buttons import Button, OptionsButton
import time


class ScreenType(Enum):
    MENU = 0
    GAME = 1
    OPTIONS = 2
    QUIT = 3
    ERROR = 4
    SCORE = 5


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
                        ScoreScreen(self.game)]

    def draw(self):
        # draw the current screen
        self.screens[self.game.current_screen.value].draw()


class Screen:
    def __init__(self, game):
        self.game = game
        self.bg_color = Colors.DARK_BLUE1
        self.buttons = []
        self.background_colour = Colors.DARK_BLUE1

    def draw(self):
        self.game.win.fill(self.background_colour)

    def show_text(self, string, x=0, y=0, color=Colors.GREEN, size=50):
        font = pygame.font.Font(self.game.current_font, size)
        text = font.render(string, True, color)
        textRect = text.get_rect()
        textRect.center = x, y
        self.game.win.blit(text, textRect)

    def process_event(self, event):
        raise NotImplementedError

    def quit_game(self):
        self.game.running = False


class MenuScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.hl_index = 0
        self.init_buttons()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.toggle_buttons((self.hl_index - 1))
            if event.key == pygame.K_DOWN:
                self.toggle_buttons((self.hl_index + 1))
            if event.key == pygame.K_RETURN:
                self.buttons[self.hl_index].execute()

    def toggle_buttons(self, new_index):
        new_index = new_index % len(self.buttons)
        self.buttons[self.hl_index].toggle_highlight()
        self.buttons[new_index].toggle_highlight()
        self.hl_index = new_index

    def init_buttons(self):

        # Main menu buttons
        self.buttons.append(Button(self.game, "Play",
                                   self.game.width//2, 360,
                                   ScreenType.GAME, size=65))

        self.buttons.append(Button(self.game, "Options",
                                   self.game.width//2, 443,
                                   ScreenType.OPTIONS, size=50))

        self.buttons.append(Button(self.game, "Quit",
                                   self.game.width//2, 513,
                                   ScreenType.QUIT, size=45, bg_color=Colors.RED))

        # Play button starts highlighted
        self.buttons[self.hl_index].toggle_highlight()

    def draw(self):
        super().draw()
        #  show title
        self.show_text("YPER", size=210, color=Colors.LIGHT_BLUE1,
                       x=self.game.width//2, y=200)

        pygame.draw.rect(self.game.win, self.background_colour,(490,135,100,45))
        #  show buttons
        for b in self.buttons:
            b.draw()


class PlayScreen(Screen):
    # TODO to time use TIMESTAMPS

    def __init__(self, game):
        super().__init__(game)
        self.started = False
        self.words = []
        self.typed_text = ""
        self.start_time = None
        self.correct_key_count = 0
        self.wpm = 0
        self.accuracy = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
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
                    self.game.wpm = (len(self.words) / total_time) * 60
                    self.game.wpm = int(self.game.wpm)
                    self.game.accuracy = (self.correct_key_count / self.total_keys) * 100
                    self.game.accuracy = round(self.game.accuracy, 2)

                    self.correct_key_count = 0
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
            self.start_time = int(time.time())

        # show words
        for word in self.words:
            word.draw()

        # show input
        self.display_input()

    def display_input(self):
        # input rectangles
        pygame.draw.rect(self.game.win, Colors.WHITE2,
                ((self.game.width//2)-225,515,430,70), border_radius=20)
        pygame.draw.rect(self.game.win, Colors.DARK_BLUE1,
                ((self.game.width//2)-220,520,420,60), border_radius=20)

        # show typed text
        self.show_text(self.typed_text, self.game.width//2, 550, Colors.WHITE1, 35)

        # icon
        self.show_text("", 300, 550, Colors.WHITE3, 65)

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

        word_list = fetch(n_paragraphs, min_words, max_words)

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


class ScoreScreen(Screen):

    def __init__(self, game):
        super().__init__(game)
        self.init_buttons()
        self.hl_index = 0

    def toggle_buttons(self, new_index):
        new_index = new_index % len(self.buttons)
        self.buttons[self.hl_index].toggle_highlight()
        self.buttons[new_index].toggle_highlight()
        self.hl_index = new_index

    def draw(self):
        super().draw()

        self.show_text("WPM", self.game.width//2, 120, Colors.WHITE1, 70)
        self.show_text(str(self.game.wpm), self.game.width//2, 190, Colors.LIGHT_BLUE2, 80)

        self.show_text("Accuracy", self.game.width//2, 300, Colors.WHITE1, 60)
        self.show_text(str(self.game.accuracy) + "%", self.game.width//2, 370, Colors.LIGHT_BLUE2, 80)

        for b in self.buttons:
            b.draw()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.toggle_buttons((self.hl_index - 1))
            if event.key == pygame.K_DOWN:
                self.toggle_buttons((self.hl_index + 1))
            if event.key == pygame.K_RETURN:
                self.buttons[self.hl_index].execute()

    def init_buttons(self):
        self.buttons.append(Button(self.game, "Play Again",
                                   self.game.width//2, (self.game.height//2) + 170,
                                   ScreenType.GAME, size=40, bg_color=Colors.WHITE1))
        self.buttons.append(Button(self.game, "Return to Menu",
                                   self.game.width//2, (self.game.height//2) + 240,
                                   ScreenType.MENU, size=40, bg_color=Colors.WHITE1))

        self.buttons[0].toggle_highlight()


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


class OptionsScreen(Screen):
    # TODO
    def __init__(self, game):
        super().__init__(game)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_screen = ScreenType.MENU

    def draw(self):
        super().draw()
        self.show_text("", x=self.game.width//2,
                       y=(self.game.height//2) - 50, size=250, color=Colors.WHITE2)
        self.show_text("coming soon", x=self.game.width//2,
                       y=(self.game.height//2) + 130, size=60, color=Colors.WHITE2)

class QuitScreen(Screen):
    # Note: This screen is not supposed to show anything. It just closes the game
    def __init__(self, game):
        super().__init__(game)

    def draw(self):
        self.quit_game()

    def process_event(self, event):
        pass
