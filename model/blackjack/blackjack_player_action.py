from enum import Enum


class PlayerAction(Enum):
    """Enumeration class for the actions available to a blackjack player."""
    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    STICK = 0
    TWIST = 1