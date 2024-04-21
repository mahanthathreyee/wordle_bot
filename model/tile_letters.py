import string

from model.tile_type import TileType
from constants.app_constants import *

class TileLetters:
    tiles: list[set[str]]
    misplaced_chars: set[str]

    def __init__(self) -> None:
        self.tiles = [set(string.ascii_lowercase) for _ in range(WORD_SIZE)]
        self.misplaced_chars = set()

        self._update_tile_func = {
            TileType.INCORRECT: self._update_incorrect,
            TileType.MISPLACED: self._update_misplaced,
            TileType.CORRECT:   self._update_correct
        }

    def update_tiles(self, word: str, tile_pattern: list[TileType]):
        for idx, ch in enumerate(word):
            try:
                self._update_tile_func[tile_pattern[idx]](idx, ch)
            except Exception as e:
                print(e)

    #region Internal Methods
    def _update_correct(self, key: int, ch: str):
        self[key] = {ch}
    
    def _update_misplaced(self, key: int, ch: str):
        self[key].discard(ch)
        self.misplaced_chars.add(ch)
    
    def _update_incorrect(self, key: int, ch: str):
        for tile in self.tiles:
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
