#region Imports
import json_fix
from enum import Enum
from pathlib import Path
#endregion

WORD_SIZE = 5
WORDLE_URL = 'https://www.nytimes.com/games/wordle/index.html'

#region Files
DATA_DIR = Path('data/')
PATTERNS_LOC                = DATA_DIR / 'patterns.csv'
WORD_LIST_LOC               = DATA_DIR / 'word_list.csv'
WORD_TREE_LOC               = DATA_DIR / 'word_tree.csv'
WORD_PATTERN_LOC            = DATA_DIR / 'word_pattern.csv'
WORD_FIRST_INFO_LOC         = DATA_DIR / 'first_info/'
WORD_FIRST_INFO_FILE_PREFIX = 'word_set'
#endregion

#region Context Keys
STATS_INFORMATION      = 'information'
STATS_PROBABILITY      = 'probability'
#endregion
