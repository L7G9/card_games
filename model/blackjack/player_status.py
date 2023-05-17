from enum import Enum


class PlayerStatus(Enum):
    """Status of a blackjack player in relation to the game.

    Attributes:
        name: A string for the status of the player in the game.
        value: An integer unique to each member in this enumeration.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    WAITING_TO_PLAY = 0
    DECIDING_ACTION = 1
    STICK = 2
    BUST = 3
