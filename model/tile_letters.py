import string

from typing import Self

from .tile_type import TileType
from constants.app_constants import *
from .wordle_exception import WordleException

class TileLetters:
    tiles: list[set[str]]
    misplaced_chars: set[str]
    correct_pos: list[str]

    def __init__(self) -> None:
        self.tiles = [set(string.ascii_lowercase) for _ in range(WORD_SIZE)]
        self.misplaced_chars = set()
        self.correct_pos = [''] * WORD_SIZE

        self._update_tile_func = {
            TileType.INCORRECT: self._update_incorrect,
            TileType.MISPLACED: self._update_misplaced,
            TileType.CORRECT:   self._update_correct
        }

    def update_tiles(self, word: str, tile_pattern: list[TileType]):
        for idx, ch in enumerate(word):
            self._update_tile_func[tile_pattern[idx]](idx, ch)


    def copy(self) -> Self:
        other = TileLetters()

        for idx, tile in enumerate(self.tiles):
            other.tiles[idx] = tile.copy()
        other.misplaced_chars = self.misplaced_chars.copy()

        return other

    #region Internal Methods
    def _update_correct(self, key: int, ch: str):
        self[key] = {ch}
        self.correct_pos[key] = ch
    
    def _update_misplaced(self, key: int, ch: str):
        self[key].discard(ch)
        self.misplaced_chars.add(ch)
    
    def _update_incorrect(self, key: int, ch: str):
        if ch in self.misplaced_chars:
            raise WordleException
        
        for idx, tile in enumerate(self.tiles):
            if self.correct_pos[idx] == ch:
                # To handle case where the character is correct in one location 
                # but is not present in any other location. If not handled, then,
                # it will accidentally delete the correct pos tile as well. This
                # will lead to that tile to have empty set
                continue
            tile.discard(ch)
    #endregion

    #region Descriptors
    def __getitem__(self, key: int) -> set[str]:
        if not isinstance(key, int):
            raise TypeError('key must be integer.')
        
        return self.tiles[key]
    
    def __setitem__(self, key: int, tile: set[str]) -> set[str]:
        if not isinstance(key, int):
            raise TypeError('key must be integer.')
        if not isinstance(tile, set):
            raise TypeError('key must be integer.')
        
        self.tiles[key] = tile
    
    def __json__(self):
        return {
            'tiles': self.tiles,
            'misplaced_chars': self.misplaced_chars,
            
            '__classname__': str(self.__class__.__name__)
        }
    #endregion
