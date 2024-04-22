import re
import json
import logging
import requests
from bs4 import BeautifulSoup

from util import file_util
from util import Pipeline

from model import Trie
from model import TileType

from constants.app_constants import *

#region Constants
WORD_LIST_PATTERN = r'\[[^\]]*?\bsnare\b[^\]]*?\]'
WORD_LIST_PATTERN = re.compile(WORD_LIST_PATTERN)
#endregion

def retrieve_store_nyt_word_list(reset_word_list_file: bool = False):
    if reset_word_list_file:
        logging.info('Resetting word list file')
        file_util.remove_file(WORD_LIST_LOC)

    if file_util.file_exists(WORD_LIST_LOC):
        logging.info('Word list file found, using existing data')
        return file_util.read_csv(WORD_LIST_LOC)

    wordle_pipeline = Pipeline(
        steps=[
            _retrieve_wordle_page,
            _extract_js_file_urls,
            _parse_all_js_files_for_words,
            _store_word_list
        ]
    )
    
    return wordle_pipeline.run(WORDLE_URL)

def build_word_tree(word_list: list[str], reset_word_tree_file: bool = False) -> Trie:
    if reset_word_tree_file:
        logging.info('Resetting word tree file')
        file_util.remove_file(WORD_TREE_LOC)

    word_tree = Trie()
    if file_util.file_exists(WORD_TREE_LOC):
        logging.info('Word tree file found, using existing data')
        word_tree.root = file_util.read_json(WORD_TREE_LOC)
        return word_tree
    
    logging.info('Building word tree')
    for word in word_list:
        word_tree += word
    
    logging.info(f'Storing word tree: {WORD_TREE_LOC}')
    file_util.write_json(word_tree.root, WORD_TREE_LOC)
    return word_tree

def retrieve_guess_patterns(reset_guess_file: bool = False):
    if reset_guess_file:
        logging.info('Resetting guess pattern file')
        file_util.remove_file(WORD_PATTERN_LOC)
    
    if file_util.file_exists(WORD_PATTERN_LOC):
        logging.info('Word pattern file found, using existing data')
        return file_util.read_csv(WORD_PATTERN_LOC)
    
    logging.info('Generating word pattern')
    patterns = _generate_pattern()

    logging.info(f'Storing word pattern: {WORD_PATTERN_LOC}')
    file_util.write_csv(patterns, WORD_PATTERN_LOC)
    return patterns

def reset_all_data():
    logging.info('Resetting all data files')
    word_list = retrieve_store_nyt_word_list(
        reset_word_list_file=True
    )

    build_word_tree(
        word_list=word_list,
        reset_word_tree_file=True
    )

    retrieve_guess_patterns(
        reset_guess_file=True
    )
#region Internal Methods
def _retrieve_wordle_page(wordle_url: str):
    logging.info(f'Retrieving Wordle page from URL: {wordle_url}')
    res = requests.get(wordle_url)
    return BeautifulSoup(res.content, features="lxml")

def _extract_js_file_urls(wordle_page: BeautifulSoup) -> list[str]:
    logging.info('Extracting JS file URLs from wordle page')
    js_files = set()
    for script_tag in wordle_page.find_all('script', type='text/javascript'):
        if script_tag.get('src'):
            js_files.add(script_tag.get('src'))
    
    logging.info(f'JS file url identified: {js_files}')
    return js_files

def _parse_js_file_for_words(js_file_url: str) -> list[str]:
    res = requests.get(js_file_url)
    js_file = str(res.content)
    
    matches = re.findall(WORD_LIST_PATTERN, js_file)
    if matches:
        return json.loads(matches[0])
    
def _parse_all_js_files_for_words(js_file_urls: list[str]) -> list[str]:
    for js_file_url in js_file_urls:
        logging.info(f'Parsing JS file url: {js_file_url}')
        word_list = _parse_js_file_for_words(js_file_url=js_file_url)
        
        logging.info(f'Word list identified: {len(word_list)} (count)')
        if word_list:
            return word_list
        
def _store_word_list(word_list: list[str]) -> list[str]:
    logging.info(f'Storing word list file at: {WORD_LIST_LOC}')
    file_util.write_csv(word_list, WORD_LIST_LOC)
    return word_list

def _generate_pattern() -> list[str]:
    logging.info('Generating patterns')
    patterns = []

    def _generate_pattern_recursively(pattern='', size_left=WORD_SIZE):
        if size_left == 0:
            patterns.append(pattern)
            return
    
        for type in TileType:
            _generate_pattern_recursively(pattern+str(type.value), size_left-1)

    _generate_pattern_recursively()
    return patterns
#endregion
