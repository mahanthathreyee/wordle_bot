from __future__ import annotations

from model import TileLetters
from util import info_gain_util
from constants.app_constants import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Context

class Wordle:
    guesses: list[str] = [''] * WORD_SIZE
    guess_tiles: list[list[TileType]] = []
    tile_letters: TileLetters = TileLetters()
    possible_words_left: set[str] = set()
    stats: dict[str, float] = {
        STATS_PROBABILITY:      0,
        STATS_INFORMATION:      0
    }

    def add_guess(self, guess: str, pattern: list[TileType], context: Context):
        self.guesses.append(guess)
        self.guess_tiles.append(pattern)
        self.tile_letters.update_tiles(guess, pattern)

        self.possible_words_left = context.word_tree.possible_words(self.tile_letters)
        self._compute_stats(context.n_words)
        
    #region Internal Methods
    def _compute_stats(self, n_words: int):
        self.stats[STATS_PROBABILITY] = info_gain_util.compute_probability(
            possible_words_count=len(self.possible_words_left), 
            total_words_count=n_words
        )
        self.stats[STATS_INFORMATION] = info_gain_util.compute_information(
            p_word=self.stats[STATS_PROBABILITY]
        )
    #endregion
