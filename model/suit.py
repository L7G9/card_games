from enum import Enum


class Suit(Enum):
    """Enumeration class for the suit of a playing card.

    Attributes:
        name: A string for the name of the suit Clubs, Diamonds, Hearts and
        Spades.  Black and Red are used for the Suit of the Jokers.
        value: An integer for the value comparitive value of each suit eg.
        Spades are worth more than Hearts.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> str:
        return self.value

    Black = 0
    Red = 1
    Clubs = 2
    Diamonds = 3
    Hearts = 4
    Spades = 5
