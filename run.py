from model import Context
from model import Wordle
from wordle import words

from util import wordle_util

if __name__ == "__main__":
    game = Wordle()
    game.add_guess(
        guess='slate',
        pattern=wordle_util.parse_int_tile_pattern('01002'),
        context=Context()
    )

    print(game.possible_words_left)
