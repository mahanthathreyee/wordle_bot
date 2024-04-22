from __future__ import annotations
import json_fix

from util import info_gain_util
from model.tile_type import TileType
from model.tile_letters import TileLetters
from constants.app_constants import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Context

class Wordle:
    guesses: list[str]
    tile_patterns: list[str]
    tile_letters: TileLetters
    possible_words_left: set[int]

    stats_probability = 0
    stats_information = 0

    def __init__(self) -> None:
        self.guesses = []
        self.tile_patterns = []
        self.tile_letters = TileLetters()
        self.possible_words_left = set()

    def add_guess(self, guess: str, pattern: list[TileType], context: Context):
        # Run first to identify conflicts with existing pattern 
        # and incoming one before making modifications
        self.tile_letters.update_tiles(guess, pattern)
        
        self.guesses.append(guess)
        self.tile_patterns.append(pattern)

        possible_words = context.word_tree.possible_words(self.tile_letters)
        for word in possible_words:
            self.possible_words_left.add(context.word_to_id_map[word])
        self._compute_stats(context.n_words)
    
    def copy(self) -> Wordle:
        other = Wordle()

        other.guesses = self.guesses.copy()
        other.tile_patterns = self.tile_patterns.copy()
        other.tile_letters = self.tile_letters.copy()
        other.stats_probability = self.stats_probability
        other.stats_information = self.stats_information

        return other
    
    def get_guess_pattern_for_db(self):
        db_str = ''
        
        for g, p in zip(self.guesses, self.tile_patterns):
            db_str += f'{g}_{p}'
        
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

    #region Decorators
    def __json__(self):
        return {
            'guess': self.guesses,
            'tile_letters': self.tile_letters,
            'possible_words_left': self.possible_words_left,
            'stats_probability': self.stats_probability,
            'stats_information': self.stats_information,

            '__classname__': str(self.__class__.__name__)
        }
    #endregion
