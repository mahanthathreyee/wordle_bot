from model import Wordle

class WordleWord:
    word: str = ''
    patterns: dict[str, Wordle] = {}
    information_gain: float = 0

    def __init__(self, word: str) -> None:
        self.word = word

    #region Internal Methods
    def __getitem__(self, key: str) -> Wordle:
        if not isinstance(key, str):
            raise TypeError('key must be string.')
        
        return self.patterns[key]
    #endregion
