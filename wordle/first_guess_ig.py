from model import Wordle
from model import Context
from model import WordleWord

from util import wordle_util
from util import info_gain_util
from constants.app_constants import *

context = Context()

def _compute_word_pattern(guess: str, pattern: str) -> Wordle:
    tile_pattern = wordle_util.parse_int_tile_pattern(pattern=pattern)
    
    game = Wordle()
    game.add_guess(
        guess=guess,
        pattern=tile_pattern,
        context=context
    )

    return game

def _compute_word(guess: str) -> WordleWord:
    patterns = context.guess_patterns
    
    wordle_patterns = {}
    for pattern in patterns:
        wordle_patterns[pattern] = _compute_word_pattern(
            guess=guess,
            pattern=pattern
        )
    
    word = WordleWord(word=guess)
    word.patterns = wordle_patterns
    
    return word

def _compute_information_gain(wordle_word: WordleWord) -> float:
    patterns = context.guess_patterns

    p_words = [0] * len(context.guess_patterns)
    i_words = [0] * len(context.guess_patterns)

    for idx, pattern in enumerate(patterns):
        p_words[idx] = wordle_word[pattern].stats_probability
        i_words[idx] = wordle_word[pattern].stats_information
    
    return info_gain_util.compute_information_gain(
        p_words=p_words, 
        i_words=i_words
    )

def compute_word_patterns(word: str) -> WordleWord:
    wordle_word = _compute_word(word)
    wordle_word.information_gain = _compute_information_gain(
        wordle_word=wordle_word
    )

    return wordle_word
