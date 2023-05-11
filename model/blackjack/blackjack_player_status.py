from enum import Enum


class BlackjackPlayerStatus(Enum):
    """Enumeration class for the status of a blackjack player."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    WAITING_TO_PLAY = 0
    WAINTING_FOR_ACTIONS = 1
    SELECTING_ACTION = 2
    STICK = 3
    BUST = 4
