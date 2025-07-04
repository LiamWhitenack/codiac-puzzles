import json

from codiac_sandbox.crud.create import get_puzzle_parameters
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES

with open("resources/old-puzzle-list.json") as f:
    data: dict[str, str]
    for data in json.load(f):
        puzzle_type = data.pop("type")
        cls = PUZZLE_CLASSES[puzzle_type]
        if missing_names := (set(get_puzzle_parameters(puzzle_type)) - set(data)):
            print(data)
            for missing_name in missing_names:
                data[missing_name] = input(missing_name)
