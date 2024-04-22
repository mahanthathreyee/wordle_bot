import math
from util import logger
from wordle import words
from wordle import first_guess_multiprocess

if __name__ == "__main__":
    logger.configure_logger()
    # words.reset_all_data()

    first_guess_multiprocess.process_word_list(
        word_list=words.retrieve_store_nyt_word_list()
    )
