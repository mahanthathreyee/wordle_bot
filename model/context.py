from __future__ import annotations

from wordle import words

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Trie

class Context:
    n_words: int = 0
    word_tree: Trie = None
    word_list: list[str] = []
    guess_patterns: list[str] = []

    def __init__(self):
        self.word_list = words.retrieve_store_nyt_word_list()
        self.n_words = len(self.word_list)

        self.word_tree: Trie = words.build_word_tree(
            word_list=self.word_list
        )

        self.guess_patterns = words.retrieve_guess_patterns()
