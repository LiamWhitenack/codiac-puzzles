from datetime import date
import json

from codiac_sandbox.puzzle_types import CryptographBase
from PySide6.QtCore import QDate, Qt


def save_as_new_file(puzzle: CryptographBase, date: QDate) -> None:
    with open(
        f"resources/by_date/{date.year()}{date.month()}{date.day()}.json", "w"
    ) as fp:
        json.dump(puzzle.to_json(all_info=True), fp, indent=2)
