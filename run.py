from wordle import words
from model import Trie

if __name__ == "__main__":
    word_list = words.retrieve_store_nyt_word_list()
    word_tree = words.build_word_tree(
        word_list=word_list
    )
