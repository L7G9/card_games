from enum import Enum


class Suit(Enum):
    """Enumeration class for the suit of a playing card.

    Suit are the standard Clubs, Diamonds, Hearts and Spades.

    Attributes:
        name: A string for the name of the suit Clubs, Diamonds, Hearts and
        Spades.
        value: An integer for the value comparative value of each suit eg.
        Spades are worth more than Hearts.
    """
    def __str__(self) -> str:
        return self.name.capitalize()

    def __int__(self) -> int:
        return self.value

    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4
