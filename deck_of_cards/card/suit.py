from enum import Enum


class Suit(Enum):
    """Enumeration class for the suit of a playing card.

    The name attribute represents the name of the suit Clubs, Diamonds, Hearts
    and Spades.  Black and Red are used for the Suit of the Jokers.
    The value attribute represents the value comparitive value of each suit
    eg. Spades are worth more than Hearts.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> str:
        return self.value

    Black = 0
    Red = 0
    Clubs = 1
    Diamonds = 2
    Hearts = 3
    Spades = 4
