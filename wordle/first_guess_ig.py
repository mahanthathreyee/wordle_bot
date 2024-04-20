from model import Context
from model import Wordle

from util import wordle_util
from constants.app_constants import *

'''
STEPS:
    1. Add word guess to wordle for each pattern
    2. Compute information gain and stats
    3. Store results to file
'''
def _guess_pattern(guess: str, pattern: str, context: Context) -> Wordle:
    tile_pattern = wordle_util.parse_int_tile_pattern(pattern=pattern)
    
    game = Wordle()
    game.add_guess(
        guess=guess,
        pattern=tile_pattern,
        context=context
    )

    return game
