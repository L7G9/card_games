from enum import Enum


class GameStatus(Enum):
    """Enumeration class for the status of a game of blackjack."""
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
