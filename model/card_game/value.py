from enum import Enum


class Value(Enum):
    """Enumeration class for the value of a playing card.

    Attributes:
        name: A string for the name of the card from Ace to King and Jokers.
        value: An integer unique to this Card in the Enumeration.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.game_value()

    def game_value(self):
        """Returns the Value of the Card for the Game it is part of.

        Override this method to implement ace high or picture cards worth 10
        for example.

        Returns:
            An integer equal to the Value of the Card in Game.
        """
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
