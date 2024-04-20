import re
import json
import requests
import math
from bs4 import BeautifulSoup

from util import file_util
from util import Pipeline

from model import Trie

from constants.app_constants import *

#region Constants
WORD_LIST_PATTERN = r'\[[^\]]*?\bsnare\b[^\]]*?\]'
WORD_LIST_PATTERN = re.compile(WORD_LIST_PATTERN)
#endregion

def retrieve_store_nyt_word_list(reset_word_list_file: bool = False):
    if reset_word_list_file:
        file_util.remove_file(WORD_LIST_LOC)

    if file_util.file_exists(WORD_LIST_LOC):
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
        file_util.remove_file(WORD_TREE_LOC)

    word_tree = Trie()
    if file_util.file_exists(WORD_TREE_LOC):
        word_tree.root = file_util.read_json(WORD_TREE_LOC)
        return word_tree
    
    for word in word_list:
        word_tree += word
    
    file_util.write_json(word_tree.root, WORD_TREE_LOC)
    return word_tree

def retrieve_guess_patterns(reset_guess_file: bool = False):
    if reset_guess_file:
        file_util.remove_file(WORD_PATTERN_LOC)
    
    if file_util.file_exists(WORD_PATTERN_LOC):
        return file_util.read_csv(WORD_PATTERN_LOC)
    
    patterns = _generate_pattern()

    file_util.write_csv(patterns, WORD_PATTERN_LOC)
    return patterns
    
#region Internal Methods
def _retrieve_wordle_page(wordle_url: str):
    res = requests.get(wordle_url)
    return BeautifulSoup(res.content, features="lxml")

def _extract_js_file_urls(wordle_page: BeautifulSoup) -> list[str]:
    js_files = set()
    for script_tag in wordle_page.find_all('script', type='text/javascript'):
        if script_tag.get('src'):
            js_files.add(script_tag.get('src'))
    
    return js_files

def _parse_js_file_for_words(js_file_url: str) -> list[str]:
    res = requests.get(js_file_url)
    js_file = str(res.content)
    
    matches = re.findall(WORD_LIST_PATTERN, js_file)
    if matches:
        return json.loads(matches[0])
    
def _parse_all_js_files_for_words(js_file_urls: list[str]) -> list[str]:
    for js_file_url in js_file_urls:
        word_list = _parse_js_file_for_words(js_file_url=js_file_url)
        if word_list:
            return word_list
        
def _store_word_list(word_list: list[str]) -> list[str]:
    file_util.write_csv(word_list, WORD_LIST_LOC)
    return word_list

def _generate_pattern() -> list[str]:
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
