import pytest

from model.blackjack.action_selector import ActionSelector
from model.blackjack.game_stats import GameStats
from model.blackjack.player_status import PlayerStatus


@pytest.fixture(scope="class")
def action_selector():
    return ActionSelector(12, 18)


class TestGameStats:
    # all players bust
    def test_should_stick_all_bust(self, action_selector):
        # all three of the other players are bust
        game_stats = GameStats(4)
        for i in range(3):
            game_stats.update(PlayerStatus.BUST)

        assert action_selector.should_stick(2, game_stats) is True

    # most players sticking or yet to play & best total >= high target
    def test_should_stick_met_high_target(self, action_selector):
        # two other other players sticking or not played yet
        game_stats = GameStats(4)
        game_stats.update(PlayerStatus.STICK)

        assert action_selector.should_stick(20, game_stats) is True

    # most players sticking or yet to play & best total < high target
    def test_should_stick_under_high_target(self, action_selector):
        # two other other players sticking or not played yet
        game_stats = GameStats(4)
        game_stats.update(PlayerStatus.STICK)

        assert action_selector.should_stick(17, game_stats) is False

    # most players bust & best total >= low target
    def test_should_stick_met_low_target(self, action_selector):
        # over half of the other players are bust
        game_stats = GameStats(4)
        for i in range(2):
            game_stats.update(PlayerStatus.BUST)

        assert action_selector.should_stick(13, game_stats) is True

    # most players bust & best total < low target
    def test_should_stick_under_low_target(self, action_selector):
        # over half of the other players are bust
        game_stats = GameStats(4)
        for i in range(2):
            game_stats.update(PlayerStatus.BUST)

        assert action_selector.should_stick(11, game_stats) is False
