from __future__ import annotations

from typing import Self, TYPE_CHECKING
from constants.app_constants import *

if TYPE_CHECKING:
    from model import TileLetters

__END__ = '__end__'

class Trie:
    root: dict[str, dict] = None

    def __init__(self, root=None) -> None:
        self.root = root or {}

    def add(self, word: str):
        node = self.root

        for ch in word:
            node[ch] = node.get(ch, {})
            node = node[ch] 
        node[__END__] = True

    def possible_words(self, tiles: TileLetters):
        possible_words = set()
        self._search_words_recursively(
            curr_word='',
            idx=0,
            node=self.root,
            possible_words=possible_words,
            tiles=tiles
        )
        return possible_words

    #region Internal Methods
    def _search_words_recursively(self, curr_word: str, idx: int, node: dict[str, dict], possible_words: set[str], tiles: TileLetters):
        if idx == WORD_SIZE:
            if tiles.misplaced_chars.issubset(curr_word):
                possible_words.add(curr_word)
            return

        valid_chars = set(node.keys()) & tiles[idx]
        for ch in valid_chars:
            self._search_words_recursively(
                curr_word=curr_word+ch,
                idx=idx+1,
                node=node[ch],
                possible_words=possible_words,
                tiles=tiles
            )
    #endregion

    #region Decorators
    def __iadd__(self, other: str) -> Self:
        if not isinstance(other, str):
            return NotImplemented
        self.add(other)
        return self
    #endregion
