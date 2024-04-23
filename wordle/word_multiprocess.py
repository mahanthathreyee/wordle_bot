#region Imports
import logging
import itertools
from tqdm import tqdm
from multiprocess import ProcessPool
from multiprocessing import Process, Manager, Queue

from util import logger
from model.context import Context
from wordle import compute_word_info
from wordle import wordle_db_process
from constants.app_constants import *
from constants.db_constants import *
#endregion

context = Context()
__STOP_PROCESS__ = '__stop_process__'

def process_info(word_list: list[str], info_level: int=1):
    if info_level == 1:
        process_first_word_list(word_list)
    elif info_level == 2:
        process_second_word_list()

def process_first_word_list(word_list: list[str]):
    logging.info(f'Computing first guess information parallely for word list (length: {len(word_list)})')

    db_queue = wordle_db_process.start_process()
    word_queue = _create_word_queue(word_list)
    progress_queue = _progress__tracker_queue(len(word_list))
    
    job_params = (word_queue, db_queue, progress_queue)
    logging.info('Starting processes to process queue')
    ProcessPool().submit(
        func=compute_word_info.process_word_queue,
        params=itertools.repeat(job_params, ProcessPool().n_process), 
        starmap=True
    )

    for word in word_list:
        word_db_info = context.read_db_conn.get_first_word_info(word)
        word_id = word_db_info[0]
        db_queue.put(
            (DB_KEY_INSERT_SECOND_WORD_STATUS, (word_id, ))
        )
    
    wordle_db_process.stop_process()
    progress_queue.put(__STOP_PROCESS__)
    logger.do_rollover()

def process_second_word_list():
    logging.info(f'Computing second guess information for top 25 fist words information gain')

    max_info_word_list = context.read_db_conn.get_first_word_max_info()
    logging.info(f'First words with max information gain: {max_info_word_list}')

    for _word_id, word, _word_info in max_info_word_list:
        _process_second_word(word)
        
        # Clear screen
        print("\033[H\033[J", end="")
        logger.do_rollover()

#region Internal Methods
def _process_second_word(base_word: str):
    logging.info(f'Computing second guess information parallely for word: {base_word}')
    base_word_info = context.read_db_conn.get_first_word_info(base_word)
    base_word_id = base_word_info[0]
    
    base_word_second_status = context.read_db_conn.get_second_word_status(base_word_id)
    if base_word_second_status and base_word_second_status[1]:
        logging.info('Word already processed, skipping computation')
        return

    db_queue = wordle_db_process.start_process()
    word_queue = _create_second_word_queue(base_word)
    progress_queue = _progress__tracker_queue(len(context.guess_patterns))
    
    job_params = (word_queue, db_queue, progress_queue)
    logging.info('Starting processes to process queue')
    ProcessPool().submit(
        func=compute_word_info.process_second_word_queue,
        params=itertools.repeat(job_params, ProcessPool().n_process), 
        starmap=True
    )
    
    db_queue.put(
        (DB_KEY_UPDATE_SECOND_WORD_STATUS, (True, base_word_id))
    )
    wordle_db_process.stop_process()
    if progress_queue:
        progress_queue.put(__STOP_PROCESS__)

def _create_word_queue(word_list: list[str]) -> Queue:
    manager = Manager()
    word_queue: Queue = manager.Queue()

    logging.info('Submitting wordlist into queue')
    for word in word_list:
        word_queue.put(word)
    
    for _ in range(ProcessPool().n_process):
        word_queue.put(__STOP_PROCESS__)

    return word_queue

def _create_second_word_queue(word: str) -> Queue:
    manager = Manager()
    second_word_queue: Queue = manager.Queue()

    logging.info('Submitting second word-pattern into queue')
    for pattern in context.guess_patterns:
        second_word_queue.put((word, pattern))
    
    for _ in range(ProcessPool().n_process):
        second_word_queue.put((__STOP_PROCESS__, None))

    return second_word_queue

def _progress__tracker_queue(n_words: int) -> Queue:
    manager = Manager()
    progress_queue = manager.Queue()
    
    tracker_process = Process(
        target=_progress_tracker,
        args=(n_words, progress_queue)
    )
    tracker_process.start()

    return progress_queue

def _progress_tracker(n_words: int, progress_queue: Queue):
        pbar = tqdm(
            total=n_words,
            desc='Word list processing'
        )

        while True:
            update = progress_queue.get()
            if update == __STOP_PROCESS__:
                break

            pbar.update(1)

#endregion
