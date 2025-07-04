import random
import re

from codiac_sandbox.hint_types import GiveALetterHint, HintBase
from codiac_sandbox.utils.make_letter_map import get_new_letter_map


class CryptographBase:
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
        self.encryptionMap = get_new_letter_map(string_to_encrypt)
        letters = list(
            s for s in string_to_encrypt.upper() if s in "QWERTYUIOPASDFGHJKLZXCVBNM"
        )
        random.shuffle(letters)
        self.hints = [GiveALetterHint(letter) for letter in letters]

    def to_json(self) -> dict[str, list | str | dict[str, str]]:
        return {k: v for k, v in self.__dict__.items() if v if not None} | dict(
            type=self.__class__.__name__, hints=[hint.to_json() for hint in self.hints]
        )


class ListPuzzle(CryptographBase):
    def __init__(self, setup: str, elements: list[str]) -> None:
        super().__init__(" ".join(elements), "list")
        self.setup = setup


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


class FamousDocumentQuote(CryptographBase):
    def __init__(self, quote: str, source: str, author: str, release_date: str):
        super().__init__(quote, "Famous Document")
        self.source = source
        self.AuthorName = author
        self.release_date = release_date


class DirectQuote(CryptographBase):
    def __init__(
        self, quote: str, author: str, release_date: str | None = None
    ) -> None:
        super().__init__(quote, "Direct Quote")
        self.author = author
        self.release_date = release_date


class GeneralPhrase(CryptographBase):
    def __init__(self, phrase: str):
        super().__init__(phrase, "General Quote")


class SongLyrics(CryptographBase):
    def __init__(self, lyrics: str, artist: str, title: str, release_date: str) -> None:
        super().__init__(lyrics, "Song lyrics")
        self.artist = artist
        self.title = title
        self.release_date = release_date


class Riddle(CryptographBase):
    def __init__(self, question: str, answer: str) -> None:
        super().__init__(answer, "Riddle")
        self.question = question


class RiddleSolvedInReverse(CryptographBase):
    def __init__(self, question: str, answer: str) -> None:
        super().__init__(question, "Reverse Riddle")
        self.answer = answer
