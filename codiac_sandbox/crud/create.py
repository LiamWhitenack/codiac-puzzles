from codiac_sandbox.gui.new_puzzle_modal import PUZZLE_CLASSES
from codiac_sandbox.puzzle_types import CryptographBase


import json


def save_puzzle(path: str, cls: type[CryptographBase], kwargs: dict[str, str]) -> None:
    with open(path) as f:
        obj = cls(**kwargs)  # type: ignore[arg-type]
        add_to = json.load(f)
    with open(path, "w") as f:
        json.dump(add_to + [obj.to_json()], f, indent=2)


def get_puzzle_parameters(puzzle_type: str) -> dict[str, inspect.Parameter]:
    cls = PUZZLE_CLASSES[puzzle_type]
    sig: dict[str, inspect.Parameter] = dict(inspect.signature(cls.__init__).parameters)  # type: ignore
    for arg in {
        "self",
        "string_to_encrypt",
        "puzzle_type",
        "hints",
        "encryptionMap",
    }:
        if arg in sig:
            del sig[arg]

    return sig
