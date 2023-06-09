"""Contains class for a player's action selector in a game of 21 Bust.

Classes:

    ActionSelector

Typical usage examples:

    player = Player(1, "John", ActionSelector(15, 20))

    stick = player.action_selector.should_stick(

        player.best_total,

        game.game_stats

    )
"""

from random import randint
from typing import Union

from model.twenty_one_bust.game_stats import GameStats


class ActionSelector:
    """Simple decision making Class for app controlled 21 Bust players.

    Has a single method that tells a player to stick if...
        1: All other players have gone bust.
        2: Most players have stuck or are yet to go and a high target total
        has been reached.
        3: Most players have gone bust and a low target total has been
        reached.

    Attributes:
        low_target: An integer representing the target hand total when the
            player should aim for a low total.
        high_target: An integer representing the target hand total when the
            player should aim for a high target.

    Raises:
        ValueError: If low_target and high_target are not within the
            range 1 to 21.
    """

    def __init__(
        self,
        low_target: Union[int, None] = None,
        high_target: Union[int, None] = None,
    ):
        """Initializes instance.

        Args:
            low_target: An integer representing the low target hand total.
                Default of None sets it to random value from 12 to 18.
            high_target: An integer representing the high target hand total.
                Default of None sets it to random value from low_target+1 to
                20.

        """
        if low_target is not None and (low_target < 1 or low_target > 21):
            raise ValueError("low_target must be in range 1 to 21")
        if high_target is not None and (high_target < 1 or high_target > 21):
            raise ValueError("low_target must be in range 1 to 21")

        if low_target is not None:
            self.low_target = low_target
        else:
            self.low_target = randint(12, 18)

        if high_target is not None:
            self.high_target = high_target
        else:
            self.high_target = randint(self.low_target + 1, 20)

    def should_stick(self, best_total: int, game_stats: GameStats) -> bool:
        """Decides if a player should stick.

        Args:
            best_total: An integer representing current best total in the
                player's hand.
            game_stats: A GameStats instance show how many players are
                sticking, have gone bust or are yet to complete their turn.

        Returns:
            A boolean set True is the player should stick and False when they
                should twist.
        """
        # remove current player from stats
        player_count = game_stats.player_count - 1
        waiting_count = game_stats.unfinished_count - 1

        all_players_bust = game_stats.bust_count == player_count
        players_not_bust = game_stats.sticking_count + waiting_count
        most_players_not_bust = players_not_bust > player_count / 2

        if all_players_bust:
            return True
        elif most_players_not_bust:
            return best_total >= self.high_target
        else:
            return best_total >= self.low_target
