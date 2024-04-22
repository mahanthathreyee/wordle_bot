from __future__ import annotations

from pathlib import Path
from util import file_util

from model.tile_type import TileType

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from model import WordleWord

def parse_int_tile_pattern(pattern: int | str) -> list[TileType]:
    if isinstance(pattern, int):
        pattern = str(pattern)

    return [TileType(int(ch)) for ch in pattern]

def compressed_first_word_info(wordle_words: dict[str, WordleWord]) -> dict[str, Any]:
    data = {}

    for word, wordle in wordle_words.items():
        data[word] = {}
        data[word]['patterns'] = {}
        
        data[word]['info_gain'] = wordle.information_gain
        for pattern, pattern_info in wordle.patterns.items():
            data[word]['patterns'][pattern] = {
                'prob': pattern_info.stats_probability,
                'info': pattern_info.stats_information
            }
    
    return data
