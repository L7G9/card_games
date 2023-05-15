from enum import Enum


class GameStatus(Enum):
    """Enumeration class for the status of a game of blackjack."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    DEALING = 0
    NEXT_PLAYER = 1
    SENDING_ACTIONS = 2
    RECEIVING_ACTION = 3
    RESOLVING = 4
    RESETTING = 5
