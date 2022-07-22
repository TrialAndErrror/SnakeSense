import os
from pathlib import Path
import json


def make_data_path():
    data_path = Path(os.getcwd(), 'data')
    data_path.mkdir(exist_ok=True, parents=True)
    return data_path


def save_json(path, data, cls=json.JSONEncoder):
    with open(path, 'w+') as file:
        json.dump(data, file, cls=cls, indent=2)


def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)
