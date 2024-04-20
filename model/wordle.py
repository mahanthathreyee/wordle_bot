from __future__ import annotations

from model import TileLetters
from constants.app_constants import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model import Context

class Wordle:
    guesses: list[str] = [''] * WORD_SIZE
    guess_tiles: list[list[TileType]] = []
    tile_letters: TileLetters = TileLetters()
    possible_words_left: set[str] = set()

    def add_guess(self, guess: str, pattern: list[TileType], context: Context):
        self.guesses.append(guess)
        self.guess_tiles.append(pattern)
        self.tile_letters.update_tiles(guess, pattern)

        self.possible_words_left = context.word_tree.possible_words(self.tile_letters)
