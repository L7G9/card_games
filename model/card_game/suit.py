from enum import Enum


class Suit(Enum):
    """Enumeration class for the suit of a playing card.

    Attributes:
        name: A string for the name of the suit Clubs, Diamonds, Hearts and
        Spades.
        value: An integer for the value comparative value of each suit eg.
        Spades are worth more than Hearts.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    Clubs = 2
    Diamonds = 3
    Hearts = 4
    Spades = 5
