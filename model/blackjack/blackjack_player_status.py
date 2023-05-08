from enum import Enum


class BlackjackPlayerStatus(Enum):
    """Enumeration class for the status of a blackjack player."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    WaitingToPlay = 0
    WaitingForActions = 1
    SelectingAction = 2
    Stick = 3
    Bust = 4
