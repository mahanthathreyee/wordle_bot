import multiprocessing
from pathlib import Path

DATA_DIR = Path('data/')
PATTERNS_LOC = DATA_DIR / 'patterns.csv'
WORD_LIST_LOC = DATA_DIR / 'word_list.csv'

JOB_POOL_PROCESS = multiprocessing.cpu_count()
