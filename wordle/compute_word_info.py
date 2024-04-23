import logging
from tqdm import tqdm
from multiprocessing import Queue

from model import Wordle
from model import WordleWord
from model import WordleException
from model import Context

from util import wordle_util
from util import info_gain_util

from constants.app_constants import *
from constants.db_constants import *

context = Context()
__STOP_PROCESS__ = '__stop_process__'

def process_word_queue(word_queue: Queue, progress_queue: Queue):
    while True:
        msg = word_queue.get()
        logging.info(f'Received message: {msg}')

        if msg == __STOP_PROCESS__:
            logging.info('Stop process signal received. Stopping process...')
            break

        msg_parts = msg.split('_')
        next_word = msg_parts[-1]
        prefix = '_'.join(msg_parts[:-1])
        logging.info(f'Computing information gain | Prefix: {prefix}, Next word: {next_word}')

        base_wordle = get_base_wordle(prefix=prefix)
        logging.info(f'Base wordle computed | Prefix: {prefix}, Next word: {next_word}')

        next_word_info = _compute_word_patterns(
            word=next_word,
            base_wordle=base_wordle.copy()
        )
        logging.info(f'Info computed: {next_word_info.information_gain} | Prefix: {prefix}, Next word: {next_word}')
        
        progress_queue.put({
            'prefix': base_wordle.get_db_prefix(),
            'next_word': next_word,
            'info_gain': next_word_info.information_gain
        })

def process_word_list_without_queue(word_list: list[str], base_wordle: Wordle) -> tuple[str, float]:
    result = [None] * len(word_list)
    
    for idx, next_word in enumerate(tqdm(word_list, desc='Word list processing (same process)', position=2, leave=False)):
        next_word_info = _compute_word_patterns(
            word=next_word,
            base_wordle=base_wordle.copy()
        )
        result[idx] = {
            'prefix': base_wordle.get_db_prefix(),
            'next_word': next_word,
            'info_gain': next_word_info.information_gain
        }
    
    max_next_word_dict = max(result, key=lambda x: x['info_gain'])
    return max_next_word_dict['next_word'], max_next_word_dict['info_gain']

def get_base_wordle(prefix) -> Wordle:
    prefix_parts = prefix.split('_')
    base_words, base_patterns = prefix_parts[::2], prefix_parts[1::2]
    
    # Default base wordle with empty guess and dummy pattern
    base_wordle = _compute_word_pattern('', context.guess_patterns[0]) if not prefix else None
    for w, p in zip(base_words, base_patterns):
        base_wordle = _compute_word_pattern(
            guess=w,
            pattern=p,
            base_wordle=base_wordle
        )
    
    return base_wordle

#region Internal Methods
def _compute_word_patterns(word: str, base_wordle: Wordle=None) -> WordleWord:
    logging.info(f'Computing info for word: {word}')
    wordle_word = _compute_word(word, base_wordle)
    wordle_word.information_gain = _compute_information_gain(
        wordle_word=wordle_word
    )

    return wordle_word

def _compute_word_pattern(guess: str, pattern: str, base_wordle: Wordle = None) -> Wordle:
    tile_pattern = wordle_util.parse_int_tile_pattern(pattern=pattern)
    
    game = base_wordle if base_wordle else Wordle()
    game.add_guess(
        guess=guess,
        pattern=tile_pattern,
        context=context
    )

    return game

def _compute_word(guess: str, base_wordle: Wordle=None) -> WordleWord:
    patterns = context.guess_patterns
    
    wordle_patterns = {}
    for pattern in patterns:
        try:
            wordle_patterns[pattern] = _compute_word_pattern(
                guess=guess,
                pattern=pattern,
                base_wordle=base_wordle.copy() if base_wordle else None
            )
        except WordleException as w_ex:
            # Exception raised if an already misplaced character is marked as 
            # incorrect character in the new pattern
            continue
    
    wordle_word = guess
    if base_wordle:
        wordle_word = base_wordle.get_db_prefix()
    
    word = WordleWord(
        word=wordle_word, 
        word_id=context.word_to_id_map[guess]
    )
    word.patterns = wordle_patterns
    
    return word

def _compute_information_gain(wordle_word: WordleWord) -> float:
    p_words = [0] * len(wordle_word.patterns)
    i_words = [0] * len(wordle_word.patterns)

    for idx, pattern in enumerate(wordle_word.patterns):
        p_words[idx] = wordle_word[pattern].stats_probability
        i_words[idx] = wordle_word[pattern].stats_information
    
    return info_gain_util.compute_information_gain(
        p_words=p_words, 
        i_words=i_words
    )
#endregion
