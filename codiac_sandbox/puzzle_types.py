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
        used: bool = False,
    ) -> None:
        if hints is None:
            hints = []
        self.string_to_encrypt = string_to_encrypt
        self.puzzle_type = puzzle_type
        self.encryption_map = get_new_letter_map(string_to_encrypt)
        letters = list(
            s for s in string_to_encrypt.lower() if s in "qwertyuiopasdfghjklzxcvbnm"
        )
        random.shuffle(letters)
        self.hints = hints + [GiveALetterHint(letter) for letter in letters]
        self.used = used

    def to_json(
        self, to_read_from_frontend: bool = False
    ) -> dict[str, list | str | dict[str, str]]:
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
        if not to_read_from_frontend:
            res |= dict(
                hints=None,
                encryption_map=None,
            )
        else:
            hints = [hint.to_json() for hint in self.hints]
            res |= dict(hints=hints, used=None, length=None)  # type: ignore[attr-defined]

        return {k: str(v) for k, v in res.items() if v is not None}

    @classmethod
    @abstractmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        """Create an instance from JSON data. Must be implemented by subclasses."""
        pass


class ListPuzzle(CryptographBase):
    def __init__(self, setup: str, elements: list[str], used: bool = False) -> None:
        super().__init__(" ".join(elements), "list", used=used)
        self.setup = setup

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            setup=data["setup"],
            elements=data["string_to_encrypt"].split(),
            used=data["used"],
        )


class CharacterQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        source_type: str,
        character_name: str,
        source: str,
        release_date: str,
        used: bool = False,
    ):
        super().__init__(quote, f"{source_type} Quote", used=used)
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
            used=data["used"],
        )


class FamousDocumentQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        source: str,
        author: str,
        release_date: str,
        used: bool = False,
    ):
        super().__init__(quote, "Famous Document", used=used)
        self.source = source
        self.author = author
        self.release_date = release_date

    @classmethod
    def from_json(
        cls,
        data: dict[str, Any],
        used: bool = False,
    ) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            source=data["source"],
            author=data["author"],
            release_date=data["release_date"],
            used=data["used"],
        )


class DirectQuote(CryptographBase):
    def __init__(
        self,
        quote: str,
        author: str,
        release_date: str | None = None,
        used: bool = False,
    ) -> None:
        super().__init__(quote, "Direct Quote", used=used)
        self.author = author
        self.release_date = release_date

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            quote=data["string_to_encrypt"],
            author=data["author"],
            release_date=data.get("release_date"),
            used=data["used"],
        )


class GeneralPhrase(CryptographBase):
    def __init__(
        self,
        phrase: str,
        used: bool = False,
    ):
        super().__init__(phrase, "General Quote", used=used)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(phrase=data["string_to_encrypt"], used=data["used"])


class SongLyrics(CryptographBase):
    def __init__(
        self,
        lyrics: str,
        artist: str,
        title: str,
        release_date: str,
        used: bool = False,
    ) -> None:
        super().__init__(lyrics, "Song lyrics", used=used)
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
            used=data["used"],
        )


class Riddle(CryptographBase):
    def __init__(
        self,
        question: str,
        answer: str,
        used: bool = False,
    ) -> None:
        super().__init__(answer, "Riddle", used=used)
        self.question = question

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question=data["question"],
            answer=data["string_to_encrypt"],
            used=data["used"],
        )


class RiddleSolvedInReverse(CryptographBase):
    def __init__(
        self,
        question: str,
        answer: str,
        used: bool = False,
    ) -> None:
        super().__init__(question, "Reverse Riddle", used=used)
        self.answer = answer

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            question=data["string_to_encrypt"], answer=data["answer"], used=data["used"]
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
