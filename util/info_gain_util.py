import numpy as np

from model import Trie

def get_possible_words(guess: str, pattern: str, word_trie: Trie):
    word_trie.reset_pos_info()
    return word_trie.find_words(guess, pattern)

def compute_probability(possible_words_count: int, total_words_count: int) -> float:
    return possible_words_count / total_words_count

def compute_information(p_word: float) -> float:
    return (-np.log2(p_word)) if p_word else 0

def compute_information_gain(p_words: list[float], i_words: list[float]) -> float:
    return np.sum(
        np.asarray(p_words) * np.asarray(i_words)
    )
