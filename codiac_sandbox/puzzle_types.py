import random
from typing import Any, Self
from abc import ABC, abstractmethod

from codiac_sandbox.hint_types import GiveALetterHint, HintBase
from codiac_sandbox.utils.make_letter_map import get_new_letter_map


class CryptographBase(ABC):
    def __init__(
        self,
        string_to_encrypt: str,
        puzzle_type: str = "Undefined",
        hints: list[HintBase] | None = None,
    ) -> None:
        if hints is None:
            hints = []
        self.string_to_encrypt = string_to_encrypt
        self.puzzle_type = puzzle_type
        self.encryption_map = get_new_letter_map(string_to_encrypt)
        letters = list(
            s for s in string_to_encrypt.upper() if s in "QWERTYUIOPASDFGHJKLZXCVBNM"
        )
        random.shuffle(letters)
        self.hints = hints + [GiveALetterHint(letter) for letter in letters]

    def to_json(self, all_info: bool = False) -> dict[str, list | str | dict[str, str]]:
        res = self.__dict__.copy()
        res = (
            dict(
                type=self.__class__.__name__,
                puzzle_type=self.puzzle_type,
                string_to_encrypt=self.string_to_encrypt,
                length=len(self.string_to_encrypt),
            )
            | res
        )
        if not all_info:
            res |= dict(
                hints=None,
                encryption_map=None,
            )
        else:
            res["hints"] = [hint.to_json() for hint in res["hints"]]

        return {k: str(v) for k, v in res.items() if v is not None}

    @classmethod
    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create an instance from JSON data. Must be implemented by subclasses."""
        pass


class ListPuzzle(CryptographBase):
    def __init__(self, setup: str, elements: list[str]) -> None:
        super().__init__(" ".join(elements), "list")
        self.setup = setup

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(setup=data["setup"], elements=data["string_to_encrypt"].split())


class CharacterQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        source_type: str,
        character_name: str,
        source: str,
        release_date: str,
    ):
        super().__init__(quote, f"{source_type} Quote")
        self.character_name = character_name
        self.source = source
        self.release_date = release_date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            source_type=data["puzzle_type"].split(" ")[0],
            character_name=data["character_name"],
            source=data["source"],
            release_date=data["release_date"],
        )


class FamousDocumentQuote(CryptographBase):
    def __init__(self, quote: str, source: str, author: str, release_date: str):
        super().__init__(quote, "Famous Document")
        self.source = source
        self.author = author
        self.release_date = release_date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            source=data["source"],
            author=data["author"],
            release_date=data["release_date"],
        )


class DirectQuote(CryptographBase):
    def __init__(
        self, quote: str, author: str, release_date: str | None = None
    ) -> None:
        super().__init__(quote, "Direct Quote")
        self.author = author
        self.release_date = release_date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            author=data["author"],
            release_date=data.get("release_date"),
        )


class GeneralPhrase(CryptographBase):
    def __init__(self, phrase: str):
        super().__init__(phrase, "General Quote")

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(phrase=data["string_to_encrypt"])


class SongLyrics(CryptographBase):
    def __init__(self, lyrics: str, artist: str, title: str, release_date: str) -> None:
        super().__init__(lyrics, "Song lyrics")
        self.artist = artist
        self.title = title
        self.release_date = release_date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            lyrics=data["string_to_encrypt"],
            artist=data["artist"],
            title=data["title"],
            release_date=data["release_date"],
        )


class Riddle(CryptographBase):
    def __init__(self, question: str, answer: str) -> None:
        super().__init__(answer, "Riddle")
        self.question = question

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question=data["question"],
            answer=data["string_to_encrypt"],
        )


class RiddleSolvedInReverse(CryptographBase):
    def __init__(self, question: str, answer: str) -> None:
        super().__init__(question, "Reverse Riddle")
        self.answer = answer

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question=data["string_to_encrypt"],
            answer=data["answer"],
        )


PuzzleClass = (
    ListPuzzle
    | CharacterQuote
    | FamousDocumentQuote
    | DirectQuote
    | GeneralPhrase
    | SongLyrics
    | Riddle
    | RiddleSolvedInReverse
)
