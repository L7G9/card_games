from model.twenty_one_bust.player_state import PlayerState


class GameStats:
    """Stats for all the stats of all player states in the game.

    Updated by the a Game instance and passed to ActionSelector to help
    decide if a plyer should stick or twist.

    Attributes:
        player_count: An integer equal to the number of players in the game.
        unfinished_count: An integer equal to the number of player yet to
          start or finish their turn.
        sticking_count: An integer equal to the number of players who have
          chosen to stick.
        bust_count: An integer equal to the number of players who have gone
          bust.
    """

    def __init__(self, player_count: int):
        """Initializes instance.

        Args:
            player_count: An integer equal to the number of players.
        """
        self.player_count = player_count
        self.unfinished_count = self.player_count
        self.sticking_count = 0
        self.bust_count = 0

    def update(self, player_state: PlayerState):
        """Updates the stats when a players' state changes.

        Should be called when a player sticks or goes bust to increase
        sticking_count or sticking_count by 1, and reduce unfinished_count
        by 1.

        Args:
            player_state: PlayerState enum member of the player who chose to
              stick or wen bust.
        """
        if self.unfinished_count == 0:
            return

        if player_state is PlayerState.STICK:
            self.sticking_count += 1
            self.unfinished_count -= 1
        elif player_state is PlayerState.BUST:
            self.bust_count += 1
            self.unfinished_count -= 1
