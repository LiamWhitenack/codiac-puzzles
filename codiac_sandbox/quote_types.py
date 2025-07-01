import random
import re

from codiac_sandbox.hint_types import GiveALetterHint, HintBase


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
        letters = list(string_to_encrypt.lower())
        random.shuffle(letters)
        self.hints = hints + [GiveALetterHint(letter) for letter in letters]


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
        source_title: str,
        release_date: int,
    ):
        super().__init__(quote, f"{source_type} Quote")
        self.character_name = character_name
        self.source_title = source_title
        self.release_date = release_date


class FamousDocumentQuote(CryptographBase):
    def __init__(
        self, quote: str, source_title: str, author_name: str, publish_date: int
    ):
        super().__init__(quote, "Famous Document")
        self.source_title = source_title
        self.AuthorName = author_name
        self.release_date = publish_date


class DirectQuote(CryptographBase):
    def __init__(self, quote: str, author: str, date: int | None = None) -> None:
        super().__init__(quote, "Direct Quote")
        self.author = author
        self.date = date


class GeneralPhrase(CryptographBase):
    def __init__(self, quote: str):
        super().__init__(quote, "General Quote")


class SongLyrics(CryptographBase):
    def __init__(self, lyric: str, artist: str, song_name: str, date: int) -> None:
        super().__init__(lyric, "Song Lyric")
        self.artist = artist
        self.song_name = song_name
        self.date = date


class Riddle(CryptographBase):
    def __init__(self, question: str, answer: str) -> None:
        super().__init__(answer, "Riddle")
        self.question = question


class RiddleSolvedInReverse(CryptographBase):
    def __init__(self, question: str, answer: str) -> None:
        super().__init__(question, "Reverse Riddle")
        self.answer = answer
