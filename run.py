import math
from util import logger
from wordle import retrieve_dataset
from wordle import first_guess_multiprocess

if __name__ == "__main__":
    logger.configure_logger()
    # words.reset_all_data()

    first_guess_multiprocess.process_word_list(
        word_list=retrieve_dataset.retrieve_store_nyt_word_list()
    )
