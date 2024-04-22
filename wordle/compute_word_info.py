import logging
from tqdm import tqdm
from multiprocessing import Queue, current_process

from model import Wordle
from model import WordleDB
from model import WordleWord
from model.context import Context
from model.wordle_exception import WordleException

from util import file_util
from util import wordle_util
from util import info_gain_util

from constants.app_constants import *
from constants.db_constants import *

context = Context()
__STOP_PROCESS__ = '__stop_process__'

def compute_word_patterns(word: str, base_wordle: Wordle=None) -> WordleWord:
    logging.info(f'Computing info for word: {word}')
    wordle_word = _compute_word(word, base_wordle)
    wordle_word.information_gain = _compute_information_gain(
        wordle_word=wordle_word
    )

    return wordle_word

def process_word_queue(word_queue: Queue, db_queue: Queue, progress_queue: Queue=None):
    info_level = 1

    while True:
        word = word_queue.get()
        if word == __STOP_PROCESS__:
            logging.info('Stopping process')
            break

        word_info_from_db = context.read_db_conn.get_first_word_info(word)
        if not word_info_from_db:
            word_info = compute_word_patterns(word)
            db_queue.put(
                (DB_KEY_INSERT_WORD_INFO, (word, word_info.information_gain, info_level))
            )
        else:
            logging.info('Word already computed, skipping computation')

        if progress_queue:
            progress_queue.put(1)

def process_second_word_queue(word_queue: Queue, db_queue: Queue, progress_queue: Queue=None):
    info_level = 2
    p_id = current_process()._identity[0] - 1

    while True:
        word, pattern = word_queue.get()
        if word == __STOP_PROCESS__:
            logging.info('Stopping process')
            break

        try:
            base_wordle = _compute_word_pattern(
                guess=word,
                pattern=pattern
            )
        except WordleException as e:
            continue
        base_word_from_db = context.read_db_conn.get_first_word_info(word)
        base_word_id = base_word_from_db[0]

        logging.info(f'Processing base word-pattern: {word}_{pattern} | Possible words: {len(base_wordle.possible_words_left)}')
        for possible_word_id in tqdm(base_wordle.possible_words_left, desc=f'Processing {word}_{pattern}', position=p_id, leave=False):
            possible_word = context.id_to_word_map[possible_word_id]
            word_info_from_db = context.read_db_conn.get_second_word_info(f'{word}_{pattern}_{possible_word}', base_word_id)
            
            if not word_info_from_db:            
                try:
                    next_word_info = compute_word_patterns(
                        word=possible_word,
                        base_wordle=base_wordle.copy()
                    )

                    db_values = (
                        f'{word}_{pattern}_{possible_word}', 
                        next_word_info.information_gain, 
                        info_level, 
                        base_word_id
                    )
                    
                    db_queue.put(
                        (DB_KEY_INSERT_WORD_INFO, db_values)
                    )
                except WordleException as e:
                    continue
            else:
                logging.info('Word already computed, skipping computation')
        
        logging.info(f'Completed processing base word-pattern: {word}_{pattern}')
        if progress_queue:
            progress_queue.put(1)

#region Internal Methods
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
        wordle_word = base_wordle.get_guess_pattern_for_db()
    
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
