import os
import csv
import json
from pathlib import Path

from typing import Any

CURRENT_WORKING_DIRECTORY = Path(os.getcwd())


def __get_absolute_file_location(relative_file_location: str) -> Path:
    return CURRENT_WORKING_DIRECTORY / relative_file_location

def file_exists(relative_file_location: str) -> bool:
    return Path(__get_absolute_file_location(relative_file_location)).exists()

def read_csv(csv_file: str | Path):
    with open(csv_file) as f:
        reader = csv.reader(f, delimiter='\n')
        return [row[0] for row in reader]
    
def read_json(json_file: str | Path):
    with open(json_file) as f:
        data = json.load(f)
        return data

def write_json(obj: Any, json_file: str | Path):
    with open(json_file, 'w') as f:
        return json.dump(obj, f)