"""Contains class for a player state error in a game of 21 Bust.

Classes:

    PlayerStateError

Typical usage examples:

    raise PlayerStateError(current_state, expected_state_list)
"""

from model.twenty_one_bust.player_state import PlayerState


class PlayerStateError(Exception):
    """Player State Error.

    Occur when the order which a method in Player is called is incompatible
    with it's state.
    For example when stick is called and the player state is BUST.
    """

    def __init__(
        self, current_state: PlayerState, expected_states: list[PlayerState]
    ):
        self.current_state = current_state
        self.expected_state = expected_states

    def __str__(self):
        return "Current State=%s Expected States=%s" % (
            self.current_state,
            self.expected_state,
        )
