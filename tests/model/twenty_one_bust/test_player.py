import pytest

from model.card_game.card import Card
from model.card_game.suit import Suit
from model.card_game.value import Value
from model.twenty_one_bust.player import Player
from model.twenty_one_bust.player_state import PlayerState


@pytest.fixture(scope="function")
def player():
    player = Player(0, "Test Player")
    player.play()
    return player


@pytest.fixture(scope="function")
def eight_of_clubs():
    return Card(Value.EIGHT, Suit.CLUBS)


@pytest.fixture(scope="function")
def ace_of_clubs():
    return Card(Value.ACE, Suit.CLUBS)


class TestPlayerClass:
    # player sticks
    def test_stick(self, player):
        assert player.stick() == PlayerState.STICK

    # player twists and does not go bust
    def test_twist_safe(self, player, eight_of_clubs):
        assert player.twist(eight_of_clubs) == PlayerState.DECIDING_ACTION

    # player twists does and goes bust
    def test_twist_bust(self, player, eight_of_clubs):
        player.add_card(eight_of_clubs)
        player.add_card(eight_of_clubs)
        assert player.twist(eight_of_clubs) == PlayerState.BUST

    # add a card to player's hand
    def test_add_card(self, player, eight_of_clubs):
        player.add_card(eight_of_clubs)
        assert eight_of_clubs in player.hand.cards
        assert player.totals == {8}
        assert player.best_total == 8

    # add non-ace card value to empty set of totals
    def test_get_totals_empty_add_card(self, player, eight_of_clubs):
        assert player.get_totals({0}, eight_of_clubs) == {8}

    # add ace values to empty set of totals
    def test_get_totals_empty_add_ace(self, player, ace_of_clubs):
        assert player.get_totals({0}, ace_of_clubs) == {1, 11}

    # add non-ace card value to set of totals containing multiple values
    def test_get_totals_multiple_add_card(self, player, eight_of_clubs):
        assert player.get_totals({1, 11}, eight_of_clubs) == {9, 19}

    # add ace values to set of totals containing multiple values
    def test_get_totals_multiple_add_ace(self, player, ace_of_clubs):
        assert player.get_totals({1, 11}, ace_of_clubs) == {2, 12, 22}

    # get best value from set with 1 safe total
    def test_get_best_total_1_safe(self, player):
        assert player.get_best_total({8}) == 8

    # get best value from set with 1 bust total
    def test_get_best_total_1_bust(self, player):
        assert player.get_best_total({25}) == 25

    # get best value from set with multiple safe total
    def test_get_best_total_multiple_safe(self, player):
        assert player.get_best_total({5, 16}) == 16

    # get best value from set safe and bust totals
    def test_get_best_total_safe_and_bust(self, player):
        assert player.get_best_total({15, 25}) == 15
