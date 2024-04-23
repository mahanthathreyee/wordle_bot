import logging
from tqdm import tqdm
from util import logger
from wordle import retrieve_dataset
from wordle import retrieve_word_info

def compute_best_first_word() -> tuple[str, float]:
    logging.info('Computing best first word')
    return retrieve_word_info.retrieve_best_word(
        prefix=''
    )

def compute_best_second_word(best_first_word: str) -> tuple[str, float]:
    res_best_word, res_info_gain = '', 0.0

    logging.info('Computing best second word')
    possible_patterns = retrieve_dataset.retrieve_guess_patterns()
    for pattern in tqdm(possible_patterns, desc='Processing second best word', position=1):
        best_word, info_gain = retrieve_word_info.retrieve_best_word(
            prefix=f'{best_first_word}_{pattern}'
        )
        if res_info_gain < info_gain:
            res_best_word = best_word
            res_info_gain = info_gain
            logging.info(f'Computing better second word: {res_best_word}, info gain: {res_info_gain}')
    
    return res_best_word, res_info_gain

if __name__ == "__main__":
    logger.configure_logger()
    # words.reset_all_data()

    best_word, info_gain = compute_best_first_word()
    logging.info(f'Best first word: {best_word}, info gain: {info_gain}')

    best_word, info_gain = compute_best_second_word(
        best_first_word=best_word
    )
    logging.info(f'Best second word: {best_word}, info gain: {info_gain}')
