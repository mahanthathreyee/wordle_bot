import logging
import itertools
from tqdm import tqdm
from multiprocess import ProcessPool
from multiprocessing import Process, Manager, Queue

from wordle import first_guess_ig
from wordle import wordle_db_process
from constants.app_constants import *

__STOP_PROCESS__ = '__stop_process__'

def process_word_list(word_list: list[str]):
    logging.info(f'Computing first guess information parallely for word list (length: {len(word_list)})')

    db_queue = wordle_db_process.start_process()
    word_queue = _create_word_queue(word_list)
    progress_queue = _progress__tracker_queue(len(word_list))
    
    job_params = (word_queue, db_queue, 1, progress_queue)
    logging.info('Starting processes to process queue')
    ProcessPool().submit(
        func=first_guess_ig.compute_words,
        params=itertools.repeat(job_params, ProcessPool().n_process), 
        starmap=True
    )
    
    wordle_db_process.stop_process()
    progress_queue.put(__STOP_PROCESS__)

#region Internal Methods
def _create_word_queue(word_list: list[str]) -> Queue:
    manager = Manager()
    word_queue: Queue = manager.Queue()

    logging.info('Submitting wordlist into queue')
    for word in word_list:
        word_queue.put(word)
    
    for _ in range(ProcessPool().n_process):
        word_queue.put(__STOP_PROCESS__)

    return word_queue

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

def _progress__tracker_queue(n_words: int) -> Queue:
    manager = Manager()
    progress_queue = manager.Queue()
    
    tracker_process = Process(
        target=_progress_tracker,
        args=(n_words, progress_queue)
    )
    tracker_process.start()

    return progress_queue

#endregion
