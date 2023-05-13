from enum import Enum


class PlayerStatus(Enum):
    """Status of a blackjack player in releation to the game.

    Attributes:
        name: A string for the status of the player in the game.
        value: An integer unique to each member in this enumeration.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    WAITING_TO_PLAY = 0
    WAITING_FOR_ACTIONS = 1
    SELECTING_ACTION = 2
    STICK = 3
    BUST = 4
