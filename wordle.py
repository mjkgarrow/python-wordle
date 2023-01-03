import requests
import curses
import os
import random
from time import sleep


class Word:
    def __init__(self, word=""):
        self.word = word

    def __repr__(self):
        return f"{self.word}"

    def __len__(self):
        return len(self.word)

    def empty(self):
        self.word = ""

    def add_letter(self, letter):
        if len(self.word) < 5:
            self.word += letter.upper()

    def remove_letter(self):
        self.word = self.word[:-1]

    def create_square_string(self):
        return "|" + "|".join(self.word.ljust(5)) + "|"

    def incorrect(self, window):
        output = self.create_square_string()
        window.erase()
        window.addstr(0, 10,
                      "Not a word!",
                      curses.color_pair(1))

        window.addstr(2, 10, output,
                      curses.color_pair(9) + curses.A_UNDERLINE)
        window.refresh()
        sleep(1)
        self.word = ""

    def check_valid(self, wordle_word):
        if self.word == wordle_word:
            return True
        else:
            return False

    def display_output(self, window, round_number, wordle_word):
        for i in range(len(repr(self.word))):
            window.addstr(2 + round_number, 10 + i, "|")
            if repr(self.word)[i] == wordle_word[i]:
                window.addstr(2 + round_number, 10 + i + 1, repr(self.word)[i],
                              curses.color_pair(2))
            elif repr(self.word)[i] in wordle_word:
                window.addstr(2 + round_number, 10 + i + 1, repr(self.word)[i],
                              curses.color_pair(4))
            else:
                window.addstr(2 + round_number, 10 + i + 1, repr(self.word)[i],
                              curses.color_pair(0))
        window.addstr(2 + round_number, 21, "|")


def check_ascii_input(key):
    ''' Check user input is alpha'''

    if (65 <= key <= 90) or (97 <= key <= 122):
        return True
    return False


def check_enter_input(key):
    ''' Check user input is enter key'''

    if key == 10 or key == 13:
        return True
    return False


def check_backspace(key):
    ''' Check user input is backspace key'''

    if key == 127:
        return True
    return False


def check_esc(key):
    ''' Check user input is esc key'''

    if key == 27:
        return True
    return False


def main(window):
    curses.curs_set(0)

    # Generate all Curser colours to be used in the app
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

    # Get 5 letter word
    # with open("words.txt", "r") as f:
    #     word_list = f.read().split(",")
    #     wordle_word = word_list[random.randint(0, len(word_list))]

    with open("words_short.txt", "r") as f:
        word_list = f.readlines()
        wordle_word = word_list[random.randint(0, len(word_list))].strip("\n")

    word = Word()
    rounds = []
    rounds.append(word)

    while True:

        window.nodelay(True)

        key = window.getch()

        if check_ascii_input(key):
            word.add_letter(chr(key))
            rounds[-1] = word
        elif check_backspace(key):
            word.remove_letter()
            rounds[-1] = word
        elif check_esc(key):
            quit()
        elif check_enter_input(key):
            if len(word) < 5:
                word.incorrect(window)
            elif repr(word) not in word_list:
                word.incorrect(window)
            elif word.check_valid(wordle_word):
                rounds.append(word)
                word.empty()
                for round in range(len(rounds)):
                    rounds[round].display_output(window, round, wordle_word)

        window.erase()
        window.addstr(0, 10,
                      "Press 'esc' to quit, 'enter' to submit guess",
                      curses.color_pair(2))

        # for round in range(len(rounds)):
        #     rounds[round].display_output(window, round, wordle_word)

        # window.addstr(2 + round, 10, rounds[round].create_square_string(),
        #               curses.A_UNDERLINE)
        # rounds[round].display_output(window, round_number, wordle_word)
        # window.addstr(2, 10, word.create_square_string(), curses.A_UNDERLINE)
        window.refresh()


def test():
    pass


if __name__ == "__main__":
    # Sets delay on escape key to 25 milliseconds
    os.environ.setdefault("ESCDELAY", "25")

    # test()
    curses.wrapper(main)
