from random import randint

from model.blackjack.game_stats import GameStats


class ActionSelector:
    """Decide if a player should stick or twist."""
    def __init__(self, low_target: int = None, high_target: int = None):
        if low_target is not None:
            self.low_target = low_target
        else:
            self.low_target = randint(12, 18)

        if high_target is not None:
            self.high_target = high_target
        else:
            self.high_target = randint(self.low_target+1, 20)

    def should_stick(self, best_total: int, game_stats: GameStats) -> bool:
        # remove current player from stats
        player_count = game_stats.player_count - 1
        waiting_count = game_stats.unfinished_count - 1

        all_players_bust = game_stats.bust_count == player_count
        players_not_bust = game_stats.sticking_count + waiting_count
        most_players_not_bust = players_not_bust > player_count/2

        if all_players_bust:
            return True
        elif most_players_not_bust:
            return best_total >= self.high_target
        else:
            return best_total >= self.low_target
