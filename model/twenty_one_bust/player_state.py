"""Contains class for state of a player in a game of 21 Bust.

Classes:

    PlayerState

Typical usage examples:

    state = PlayerState.STICK
"""


from enum import Enum


class PlayerState(Enum):
    """state of a player in a game of 21 Bust.

    Attributes:
        name: A string for the state of the player in the game.
        value: An integer unique to each member in this enumeration.
    """

    def __str__(self) -> str:
        return self.name

    def __int__(self) -> int:
        return self.value

    WAITING_TO_PLAY = 0
    DECIDING_ACTION = 1
    STICK = 2
    BUST = 3
