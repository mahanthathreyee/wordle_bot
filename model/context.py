from __future__ import annotations

from util import logger
from model import WordleDB
from wordle import retrieve_dataset

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Trie

class Context:
    n_words: int = 0
    word_tree: Trie = None
    word_list: list[str] = []
    guess_patterns: list[str] = []
    word_to_id_map: dict[str, int] = {}
    id_to_word_map: dict[str, int] = {}
    read_db_conn: WordleDB = None

    def __init__(self):
        logger.configure_logger()
        
        self.word_list = retrieve_dataset.retrieve_store_nyt_word_list()
        self.n_words = len(self.word_list)

        self.word_tree: Trie = retrieve_dataset.build_word_tree(
            word_list=self.word_list
        )

        self.guess_patterns = retrieve_dataset.retrieve_guess_patterns()

        self.word_to_id_map = self._generate_word_to_id()
        self.id_to_word_map = self._generate_id_to_word()

        self.read_db_conn = WordleDB(readonly=True)

    #region Internal Methods
    def _generate_word_to_id(self) -> dict[str, int]:
        res = {}
        for idx, word in enumerate(self.word_list):
            res[word] = idx
        
        return res
        
    def _generate_id_to_word(self) -> dict[str, int]:
        res = {}
        for idx, word in enumerate(self.word_list):
            res[idx] = word
        
        return res
    #endregion

    #region Decorators
    def __json__(self):
        return {
            'n_words': self.n_words,
            'word_tree': self.word_tree,
            'word_list': self.word_list,
            'guess_patterns': self.guess_patterns,

            '__classname__': str(self.__class__.__name__)
        }
    #endregion
