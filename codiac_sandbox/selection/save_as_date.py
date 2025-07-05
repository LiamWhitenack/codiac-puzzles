from datetime import date
import json

from codiac_sandbox.puzzle_types import CryptographBase


def save_as_new_file(puzzle: CryptographBase, date: date) -> None:
    save: dict = puzzle.to_json()
    save = save | dict(
        encryption_map=puzzle.encryption_map,
        hints=[hint.to_json() for hint in puzzle.hints],
    )
    with open(f"resources/by_date/{date.year}{date.month}{date.day}.json") as fp:
        json.dump(save, fp)
