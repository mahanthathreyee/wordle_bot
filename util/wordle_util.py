from constants.app_constants import *

def parse_int_tile_pattern(pattern: int | str) -> list[TileType]:
    if isinstance(pattern, int):
        pattern = str(pattern)

    return [TileType(int(ch)) for ch in pattern]
