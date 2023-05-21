import pytest

from model.blackjack.game_stats import GameStats
from model.blackjack.player_state import PlayerState


@pytest.fixture(scope="function")
def game_stats():
    return GameStats(4)


class TestGameStats:
    # update game stats when a player sticks
    def test_update_stick(self, game_stats):
        game_stats.update(PlayerState.STICK)
        assert game_stats.unfinished_count == 3
        assert game_stats.sticking_count == 1

    # update game stats when a player goes bust
    def test_update_bust(self, game_stats):
        game_stats.update(PlayerState.BUST)
        assert game_stats.unfinished_count == 3
        assert game_stats.bust_count == 1
