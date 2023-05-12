from enum import Enum


class PlayerStatus(Enum):
    """Enumeration class for the status of a blackjack player."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    WAITING_TO_PLAY = 0
    WAITING_FOR_ACTIONS = 1
    SELECTING_ACTION = 2
    STICK = 3
    BUST = 4