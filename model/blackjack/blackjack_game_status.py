from enum import Enum


class BlackjackGameStatus(Enum):
    """Enumeration class for the status of a game of blackjack."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    Dealing = 0
    SendingActions = 1
    ReceivingAction = 2
    Resolving = 3
    Resetting = 4
