class HintBase:
    pass


class GiveALetterHint(HintBase):
    def __init__(self, letter: str) -> None:
        self.letter = letter
