"""Contains class for a player order error in a game of 21 Bust.

Classes:

    PlayerOrderError

Typical usage examples:

    raise PlayerOrderError(player, expected_player)
"""

from model.twenty_one_bust.player import Player


class PlayerOrderError(Exception):
    """Player Order Error.

    Occur when a player is passed to a method which would make the player
    perform some action and is not that player's turn.
    """

    def __init__(
        self, current_player: Player, expected_player: Player
    ):
        self.current_player = current_player
        self.expected_player = expected_player

    def __str__(self):
        return "Player=%s Expected Player=%s" % (
            self.current_player.name,
            self.expected_player.name,
        )
