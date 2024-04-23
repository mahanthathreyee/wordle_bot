import logging

import util
import model
import wordle
import multiprocess

from util import logger
from util import wordle_util
from model import Wordle
from model.context import Context
from wordle import retrieve_word_info

context = Context()

if __name__ == "__main__":
    logger.configure_logger()

    game = Wordle()

    for _ in range(6):
        best_word, info_gain = retrieve_word_info.retrieve_best_word(
            prefix=game.get_db_prefix(),
            skip_db_store=True
        )
        print(f'Best word: {best_word}')

        pattern = input('Pattern: ')
        if pattern == 'exit': 
            break
        
        game.add_guess(
            guess=best_word,
            pattern=wordle_util.parse_int_tile_pattern(pattern),
            context=context
        )

    