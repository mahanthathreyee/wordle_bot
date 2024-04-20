from __future__ import annotations

from util import info_gain_util
from constants.app_constants import *
from model.tile_letters import TileLetters

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Context
class Wordle:
    guesses: list[str]
    guess_tiles: list[list[TileType]]
    tile_letters: TileLetters
    possible_words_left: set[str]

    stats_probability = 0
    stats_information = 0

    def __init__(self) -> None:
        self.guesses = []
        self.guess_tiles = []
        self.tile_letters = TileLetters()
        self.possible_words_left = set()

    def add_guess(self, guess: str, pattern: list[TileType], context: Context):
        self.guesses.append(guess)
        self.guess_tiles.append(pattern)
        self.tile_letters.update_tiles(guess, pattern)

        self.possible_words_left = context.word_tree.possible_words(self.tile_letters)
        self._compute_stats(context.n_words)
        
    #region Internal Methods
    def _compute_stats(self, n_words: int):
        self.stats_probability = info_gain_util.compute_probability(
            possible_words_count=len(self.possible_words_left), 
            total_words_count=n_words
        )
        self.stats_information = info_gain_util.compute_information(
            p_word=self.stats_probability
        )
    #endregion
