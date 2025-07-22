from datetime import datetime, timedelta
import json
from random import choice
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES, parse_puzzle

tomorrow = datetime.now() + timedelta(days=1)

with open("resources/master-puzzle-list.json", "r") as read:
    with open(
        f"resources/auto-generated/{tomorrow.strftime('%Y%m%d')}.json", "w"
    ) as write:
        puzzle = parse_puzzle(choice(json.load(read)))
        data = puzzle.to_json(to_read_from_frontend=True)

        json.dump(data, write, indent=2)
