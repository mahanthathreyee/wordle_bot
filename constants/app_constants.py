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

#region Database
DB_HOST     = 'localhost'
DB_USER     = 'wordle_bot'
DB_PASSWORD = 'abcd1234'
DB_NAME     = 'wordle'
#endregion

#region SQL Queries
INSERT_INFO_GAIN     = 'INSERT INTO information_gain (word, info_gain, info_level) \
                            VALUES (%s, %s, %s)                                       \
                            ON CONFLICT DO NOTHING'
SELECT_WORD_INFO     = 'SELECT * FROM information_gain WHERE word=%s'
SELECT_WORD_MAX_INFO = 'SELECT word, info_gain FROM information_gain WHERE info_gain=( \
                            SELECT MAX(info_gain) FROM information_gain                \
                                WHERE info_level=%s                                    \
                        );'
#endregion
