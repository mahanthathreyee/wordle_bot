from .wordle import Wordle

from constants.app_constants import *

class WordleWord:
    word: str = ''
    word_id: int = 0
    patterns: dict[str, Wordle]
    information_gain: float = 0

    def __init__(self, word: str, word_id: int) -> None:
        self.word = word
        self.word_id = word_id
        self.patterns = {}

    #region Internal Methods
    def __getitem__(self, key: str) -> Wordle:
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        
        return self.patterns[key]
    #endregion

    #region Decorators
    def __json__(self):
        return {
            'word': self.word,
            'patterns': self.patterns,
            'information_gain': self.information_gain,

            '__classname__': str(self.__class__.__name__)
        }
    #endregion
