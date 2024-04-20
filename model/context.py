from model import Trie
from wordle import words

class Context:
    word_list: list[str] = []
    word_tree: Trie = None

    def __init__(self):
        self.word_list = words.retrieve_store_nyt_word_list()
        self.word_tree: Trie = words.build_word_tree(
            word_list=self.word_list
        )
