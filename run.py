from util import logger
from wordle import words
from wordle import first_guess_multiprocess
from constants import multiprocess_constant

if __name__ == "__main__":
    logger.configure_logger()

    # words.reset_all_data()
    
    word_list = words.retrieve_store_nyt_word_list()
    items_per_job = 500

    first_guess_multiprocess.process_word_list(
        word_list=word_list,
        items_per_job=items_per_job
    )
