from enum import Enum


class Value(Enum):
    """Enumeration class for the value of a playing card.

    The name attribute represents
    The value attribute represents the value of the card in the game.

    Attributes:
        name: A string for the name of the card from Ace to King and Jokers.
        value: An integer for the value of the card in the game.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    def game_value(self):
        return self.value

    Joker = 0
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
