import curses
import os
import random
from time import sleep


class Word:
    def __init__(self, word=""):
        self.word = word
        self.index = 0

    def __repr__(self):
        return f"{self.word}"

    def __len__(self):
        return len(self.word)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.word):
            raise StopIteration
        else:
            char = self.word[self.index]
            self.index += 1
            return char

    def __getitem__(self, index: int):
        return self.word[index]

    def empty(self):
        self.word = ""

    def add_letter(self, letter):
        if len(self.word) < 5:
            self.word += letter.upper()

    def remove_letter(self):
        self.word = self.word[:-1]

    def create_square_string(self):
        return "|" + "|".join(self.word.ljust(5)) + "|"

    def check_correct(self, wordle_word):
        return self.word == wordle_word

    def incorrect(self, window, round_number, window_sizes):
        for i in range(len(self.word)):
            window.addstr(window_sizes[1] + 3 + round_number,
                          window_sizes[0] + 15 + (i * 2),
                          self.word[i],
                          curses.color_pair(1) + curses.A_UNDERLINE)
            window.addstr(window_sizes[1] + 3 + round_number,
                          window_sizes[0] + 14 + (i * 2),
                          "|",
                          curses.A_UNDERLINE)
        window.addstr(window_sizes[1] + 3 + round_number,
                      window_sizes[0] + 24,
                      "|",
                      curses.A_UNDERLINE)
        window.refresh()
        sleep(1)
        self.word = ""

    def accurate_letters(self, wordle_word):
        letters = []
        for i in range(len(self.word)):
            if self.word[i] == wordle_word[i]:
                letters.append(self.word[i])
        return letters

    def display_output(self, window, round_number, wordle_word, window_sizes):
        not_found = wordle_word

        for i in range(len(self.word)):
            if (self.word[i] == wordle_word[i]):
                not_found = not_found.replace(self.word[i], '', 1)
                window.addstr(window_sizes[1] + 3 + round_number,
                              window_sizes[0] + 15 + (i * 2),
                              self.word[i],
                              curses.color_pair(2) + curses.A_UNDERLINE)
            else:
                window.addstr(window_sizes[1] + 3 + round_number,
                              window_sizes[0] + 15 + (i * 2),
                              self.word[i],
                              curses.color_pair(0) + curses.A_UNDERLINE)

        for i in range(len(self.word)):
            if (self.word[i] in not_found) & (self.word[i] != wordle_word[i]):
                not_found = not_found.replace(self.word[i], '', 1)
                window.addstr(window_sizes[1] + 3 + round_number,
                              window_sizes[0] + 15 + (i * 2),
                              self.word[i],
                              curses.color_pair(215) + curses.A_UNDERLINE)

            window.addstr(window_sizes[1] + 3 + round_number,
                          window_sizes[0] + 14 + (i * 2),
                          "|",
                          curses.A_UNDERLINE)
        window.addstr(window_sizes[1] + 3 + round_number,
                      window_sizes[0] + 24,
                      "|",
                      curses.A_UNDERLINE)


def get_window_sizes():
    ''' Find the size of the terminal window and 
    calculate maximum string width and starting positions'''

    # Get terminal window size [width, height]
    window_size = [os.get_terminal_size()[0], os.get_terminal_size()[1]]

    # Calculate starting positions based on width and window size
    text_start_x = (window_size[0]//2) - 30
    text_start_y = (window_size[1]//2) - 7
    return [text_start_x, text_start_y]


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


def print_keyboard(window, accurate_letters,
                   correct_letters, used_letters, window_sizes):
    keyboard = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                [' ', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                [' ', ' ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']]

    # Print keyboard
    for i in range(len(keyboard)):
        for j in range(len(keyboard[i])):
            if keyboard[i][j].upper() in accurate_letters:
                window.addstr(window_sizes[1] + 11 + i,
                              window_sizes[0] + 10 + (j * 2),
                              keyboard[i][j],
                              curses.color_pair(2))
            elif keyboard[i][j].upper() in correct_letters:
                window.addstr(window_sizes[1] + 11 + i,
                              window_sizes[0] + 10 + (j * 2),
                              keyboard[i][j],
                              curses.color_pair(215))
            elif keyboard[i][j].upper() in used_letters:
                window.addstr(window_sizes[1] + 11 + i,
                              window_sizes[0] + 10 + (j * 2),
                              " ",
                              curses.color_pair(0))
            else:
                window.addstr(window_sizes[1] + 11 + i,
                              window_sizes[0] + 10 + (j * 2),
                              keyboard[i][j],
                              curses.color_pair(0))


def play_game(window, rounds, round, word_list, wordle_word, used_letters, correct_letters, accurate_letters):

    while True:
        # Get terminal size so game is centred
        window_sizes = get_window_sizes()  # [x,y]

        window.nodelay(True)

        # Get user input
        key = window.getch()

        if check_ascii_input(key):
            rounds[round].add_letter(chr(key))
            used_letters.append(rounds[round][-1])
            used_letters = used_letters[: (round * 5) + 5]
        elif check_backspace(key):
            rounds[round].remove_letter()
            if len(rounds[round]) == 0:
                if len(used_letters) % 5 != 0:
                    used_letters = used_letters[:-1]
            else:
                used_letters = used_letters[:-1]
        elif key == 9:
            round = 6
        elif check_esc(key):
            quit()
        elif check_enter_input(key):
            if len(rounds[round]) == 0:
                continue
            if (len(rounds[round]) < 5) or (repr(rounds[round]) not in word_list):
                used_letters = used_letters[:-len(rounds[round])]
                rounds[round].incorrect(window, round, window_sizes)

            elif rounds[round].check_correct(wordle_word):

                # Display correct word colouring
                rounds[round].display_output(window, round,
                                             wordle_word, window_sizes)

                # Display winning prompt
                window.nodelay(False)
                window.move(0, 10)
                window.clrtoeol()
                if round == 0:
                    window.addstr(window_sizes[1] + 3 + round,
                                  window_sizes[0] + 30,
                                  f"You got it right in {round + 1} round! Press any button to restart",
                                  curses.color_pair(2))
                else:
                    window.addstr(window_sizes[1] + 3 + round,
                                  window_sizes[0] + 30,
                                  f"You got it right in {round + 1} rounds! Press any button to restart",
                                  curses.color_pair(2))

                # Reset game
                round = 0
                used_letters = []
                correct_letters = []
                accurate_letters = []
                for line in rounds:
                    line.empty()
                wordle_word = word_list[random.randint(0, len(word_list))]

                window.refresh()

                # Wait for user to press key
                key = window.getch()

            else:
                # Update current round
                round += 1

                # Generate lists of correct letters for keyboard
                correct_letters = [char for char in
                                   used_letters if char in wordle_word]

                accurate_letters = [item for sublist in
                                    [x.accurate_letters(wordle_word) for
                                     x in rounds] for item in sublist]

        # Clear screen
        window.erase()

        # Round 6 means game is over
        if round == 6:
            window.addstr(window_sizes[1] + 2,
                          window_sizes[0] + 10,
                          f"You lost! The word was {wordle_word}",
                          curses.color_pair(3))
            window.refresh()

            # Reset game
            for line in rounds:
                line.empty()
            round = 0
            used_letters = []
            correct_letters = []
            accurate_letters = []
            wordle_word = word_list[random.randint(0, len(word_list))].upper()
            sleep(2)
            continue
        else:
            window.addstr(window_sizes[1],
                          window_sizes[0] - 10,
                          "Press 'esc' to quit, 'enter' to submit guess, 'tab' to see answer",
                          curses.color_pair(4))

            for line in range(len(rounds)):
                if line < round:
                    rounds[line].display_output(window, line,
                                                wordle_word, window_sizes)
                else:
                    window.addstr(window_sizes[1] + 3 + line,
                                  window_sizes[0] + 14,
                                  rounds[line].create_square_string(),
                                  curses.A_UNDERLINE)

        print_keyboard(window, accurate_letters,
                       correct_letters, used_letters, window_sizes)

        window.refresh()


def main(window):
    curses.curs_set(0)

    # Generate all Curser colours to be used in the app
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1)

    # Get random 5-letter word
    with open("words.txt", "r") as f:
        word_list = f.read().upper().splitlines()
        wordle_word = word_list[random.randint(0, len(word_list))]

    # Initialise game variables
    rounds = [Word(), Word(), Word(), Word(), Word(), Word()]
    round = 0
    used_letters = []
    correct_letters = []
    accurate_letters = []

    # Play game loop
    play_game(window, rounds, round, word_list, wordle_word,
              used_letters, correct_letters, accurate_letters)


if __name__ == "__main__":
    # Sets delay on escape key to 25 milliseconds
    os.environ.setdefault("ESCDELAY", "25")

    curses.wrapper(main)
