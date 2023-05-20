from enum import Enum


class Value(Enum):
    """Enumeration class for the value of a playing card.

    Values for cards in a standard deck of cards where Aces are worth 1 and
    Kings are worth 13.

    Attributes:
        name: A string for the name of the card from Ace to King.
        value: An integer unique to this Card in the Enumeration.
    """
    def __str__(self) -> str:
        return self.name.capitalize()

    def __int__(self) -> int:
        return self.game_value()

    def game_value(self):
        """Returns the Value of the Card for the Game it is part of.

        Edit this method to implement ace high or picture cards worth 10
        for example.

        Returns:
            An integer equal to the Value of the Card in Game.
        """
        return self.value

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
