import json
import logging
from tqdm import tqdm
from multiprocessing import current_process

from model import Wordle
from model import Context
from model import WordleWord

from util import file_util
from util import wordle_util
from util import info_gain_util
from constants.app_constants import *

context = Context()

def compute_word_patterns(word: str) -> WordleWord:
    logging.info(f'Computing info for word: {word}')
    wordle_word = _compute_word(word)
    wordle_word.information_gain = _compute_information_gain(
        wordle_word=wordle_word
    )

    return wordle_word

def compute_words(words: list[str], job_id: int=0) -> dict[str, WordleWord]:
    words_ig = {}
    first_info_file = f'{WORD_FIRST_INFO_LOC}/{WORD_FIRST_INFO_FILE_PREFIX}_{len(words)}_{job_id}.json'

    if file_util.file_exists(first_info_file):
        logging.info('Word job already completed, skipping computation')
        return
    
    logging.info(f'Computing info for word list - length {len(words)} ')
    p_id = current_process()._identity[0] - 1
    for word in tqdm(words, desc=f'Word list part {job_id}', position=p_id):
        words_ig[word] = compute_word_patterns(word)
    
    logging.info(f'Storing all words info to file: {first_info_file}')
    compressed_data = wordle_util.compressed_first_word_info(words_ig)
    file_util.write_json(
        obj=json.dumps(compressed_data),
        json_file=first_info_file
    )

    return words_ig

#region Internal Methods
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
    
    word = WordleWord(
        word=guess, 
        word_id=context.word_to_id_map[guess]
    )
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
#endregion
