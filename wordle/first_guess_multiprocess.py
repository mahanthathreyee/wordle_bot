import json
import logging
import multiprocess
from multiprocess import ProcessPool

from util import file_util
from wordle import first_guess_ig
from constants.app_constants import *

def process_word_list(word_list: list[str], items_per_job: int):
    logging.info(f'Computing first guess information parallely for word list (length: {len(word_list)})')
    words_per_job = multiprocess.generate_jobs(
        data=word_list,
        items_per_job=items_per_job
    )

    words_per_job = [
        (words_job, idx) for idx, words_job in enumerate(words_per_job)
    ]

    logging.info('Submitting wordlist into separate processes')
    ProcessPool().submit(
        func=first_guess_ig.compute_words,
        params=words_per_job, 
        starmap=True
    )
