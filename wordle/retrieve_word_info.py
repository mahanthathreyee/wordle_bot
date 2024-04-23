#region Imports
import logging
import itertools
from tqdm import tqdm
from multiprocess import ProcessPool
from multiprocessing import Process, Manager, Queue
\
from model import Context
from model import WordleException

from wordle import compute_word_info
from constants.app_constants import *
from constants.db_constants import *
#endregion

context = Context()
__STOP_PROCESS__ = '__stop_process__'

def retrieve_best_word(prefix: str) -> tuple[str, float]:
    logging.info(f'Retrieving word with max info for prefix: {prefix}')

    db_result = context.db_conn.get_prefix(prefix=prefix)
    if db_result:
        logging.info(f'Found result in DB | Prefix: {prefix}, Word: {db_result[0]}, Info Gain: {db_result[1]}')
        return db_result[0], db_result[1]

    logging.info(f'Prefix not found in DB, proceeding to computation | Prefix: {prefix}')
    next_word, info_gain = _compute_best_word_for_prefix(prefix=prefix)
    context.db_conn.insert_prefix(
        prefix=prefix,
        word=next_word,
        info_gain=info_gain
    )

    return next_word, info_gain

#region Internal Methods
def _compute_best_word_for_prefix(prefix: str) -> tuple[str, float]:
    logging.info(f'Computing base wordle | Prefix: {prefix}')
    try:
        base_wordle = compute_word_info.get_base_wordle(
            prefix=prefix
        )
    except WordleException as w:
        logging.info(f'Current prefix is invalid, skipping computation | Prefix: {prefix}')
        return '', 0.0

    word_list = base_wordle.possible_words_left
    word_list = [context.id_to_word_map[word_id] for word_id in word_list]
    logging.info(f'Possible words to compute: {len(word_list)} | Prefix: {prefix}')

    if len(word_list) == 0:
        logging.info(f'No words possible with current prefix, skipping computation | Prefix: {prefix}')
        return '', 0.0
    
    if len(word_list) <= 150:
        return compute_word_info.process_word_list_without_queue(
            word_list=word_list,
            base_wordle=base_wordle
        )
    else:
        return _compute_best_word_parallely(
            word_list=word_list,
            prefix=prefix
        )

def _compute_best_word_parallely(word_list: list[str], prefix: str) -> tuple[str, float]:
    logging.info(f'Creating queues | Prefix: {prefix}')
    word_queue = _create_word_queue(word_list, prefix)
    result_process, result_queue, result = _create_result_queue(len(word_list))
    
    logging.info(f'Starting processes for computation | Prefix: {prefix}')
    ProcessPool().submit(
        func=compute_word_info.process_word_queue,
        params=itertools.repeat((word_queue, result_queue), ProcessPool().n_process), 
        starmap=True
    )
    
    result_queue.put(__STOP_PROCESS__)
    result_process.join()
    max_next_word_dict = max(result, key=lambda x: x['info_gain'])
    
    return max_next_word_dict['next_word'], max_next_word_dict['info_gain']

def _create_word_queue(word_list: list[str], prefix: str) -> Queue:
    manager = Manager()
    second_word_queue: Queue = manager.Queue()

    logging.info(f'Submitting second word-pattern into queue | Prefix: {prefix}')
    for word in word_list:
        second_word_queue.put(
            f'{prefix}_{word}' if prefix else word
        )

    for _ in range(ProcessPool().n_process):
        second_word_queue.put(__STOP_PROCESS__)

    return second_word_queue

def _create_result_queue(n_words: int) -> tuple[Process, Queue]:
    manager = Manager()
    result_queue = manager.Queue()
    result = manager.list()
    
    result_process = Process(
        target=_progress_tracker,
        args=(n_words, result_queue, result)
    )
    result_process.start()

    return result_process, result_queue, result

def _progress_tracker(n_words: int, result_queue: Queue, result: list):
    pbar = tqdm(total=n_words, desc='Word list processing (parallel)', position=2, leave=False)

    while True:
        computation_res = result_queue.get()
        if isinstance(computation_res, str) and computation_res == __STOP_PROCESS__:
            break
        result.append(computation_res)
        pbar.update(1)
    
    return result
#endregion
