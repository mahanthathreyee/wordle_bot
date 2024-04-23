import math
from util import logger
from wordle import retrieve_dataset
from wordle import word_multiprocess

if __name__ == "__main__":
    logger.configure_logger()
    # words.reset_all_data()

    word_multiprocess.process_info(
        word_list=retrieve_dataset.retrieve_store_nyt_word_list(),
        info_level=2
    )
