from enum import Enum


class GameStatus(Enum):
    """Enumeration class for the status of a game of blackjack."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    DEALING = 0
    SENDING_ACTIONS = 1
    RECEIVING_ACTION = 2
    RESOLVING = 3
    RESETTING = 4
