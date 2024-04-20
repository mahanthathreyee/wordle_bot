#region Imports
from enum import Enum
from pathlib import Path
#endregion

WORD_SIZE = 5
WORDLE_URL = 'https://www.nytimes.com/games/wordle/index.html'

#region Enums
TileType = Enum('TileType', ['INCORRECT', 'MISPLACED', 'CORRECT'], start=0)
#endregion

#region Files
DATA_DIR = Path('data/')
PATTERNS_LOC     = DATA_DIR / 'patterns.csv'
WORD_LIST_LOC    = DATA_DIR / 'word_list.csv'
WORD_TREE_LOC    = DATA_DIR / 'word_tree.csv'
WORD_PATTERN_LOC = DATA_DIR / 'word_pattern.csv'
#endregion

#region Context Keys
STATS_INFORMATION      = 'information'
STATS_PROBABILITY      = 'probability'
#endregion
