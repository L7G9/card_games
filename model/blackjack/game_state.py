from enum import Enum


class GameState(Enum):
    """State of a blackjack game.

    Attributes:
        name: A string for the State of the game.
        value: An integer unique to each member in this enumeration.
    """

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    DEALING = 0
    GETTING_NEXT_PLAYER = 1
    STARTING_PLAYER_TURN = 2
    WAITING_FOR_PLAYER = 3
    RESOLVING_GAME = 4
    RESETTING_GAME = 5
