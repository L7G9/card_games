from model.blackjack.game_stats import GameStats


class ActionSelector:
    """Decide if a player should stick or twist."""
    def __init__(self, low_target: int, high_target: int):
        self.low_target = low_target
        self.high_target = high_target

    def should_stick(self, best_total: int, game_stats: GameStats) -> bool:
        all_players_bust = game_stats.bust_count == game_stats.player_count
        players_not_bust = game_stats.sticking_count+game_stats.waiting_count
        most_players_not_bust = players_not_bust > game_stats.player_count/2

        if all_players_bust:
            return True
        elif most_players_not_bust:
            return best_total >= self.high_target
        else:
            return best_total >= self.low_target
