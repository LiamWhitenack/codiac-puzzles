import inspect
import types
from typing import Union, get_args, get_origin
import typing
from codiac_sandbox.utils.puzzle_classes import PUZZLE_CLASSES
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
    for param_name, param in sig.copy().items():
        if param_name in {
            "self",
            "string_to_encrypt",
            "puzzle_type",
            "hints",
            "encryptionMap",
        } or annotation_allows_none(param):
            del sig[param_name]

    return sig


def annotation_allows_none(param: inspect.Parameter) -> bool:
    annotation = param.annotation

    # If annotation is not set
    if annotation is inspect.Parameter.empty:
        return False

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is types.UnionType or origin is typing.Union:
        return type(None) in args

    return False
