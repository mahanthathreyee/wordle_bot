import os
import csv
import json
import shutil
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
    
def write_csv(obj: Any, csv_file: str | Path, delimiter='\n'):
    with open(csv_file, 'w') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(obj)
    
def read_json(json_file: str | Path):
    with open(json_file) as f:
        data = json.load(f)
        return data

def write_json(obj: Any, json_file: str | Path):
    with open(json_file, 'w') as f:
        return json.dump(obj, f)
    
def remove_file(file: str | Path):
    if file_exists(file):
        os.remove(file)

def create_folder(folder: str | Path):
    folder_pth = Path(folder)
    folder_pth.mkdir(parents=True, exist_ok=True)

def remove_folder(folder: str | Path):
    shutil.rmtree(folder)
