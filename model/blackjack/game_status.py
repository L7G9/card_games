from enum import Enum


class GameStatus(Enum):
    """Status of a blackjack game.

    Attributes:
        name: A string for the status of the game.
        value: An integer unique to each member in this enumeration.
    """
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    DEALING = 0
    STARTING_PLAYER = 1
    GETTING_PLAYER_ACTION = 2
    RESOLVING_PLAYER_ACTION = 3
    RESOLVING_GAME = 4
    RESETTING_GAME = 5
