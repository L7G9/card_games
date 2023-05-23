import pytest

from model.card_game.deck import Deck
from model.card_game.player import Player
from model.card_game.suit import Suit
from model.card_game.value import Value


@pytest.fixture(scope="class")
def deck():
    return Deck("Test Deck", Value, Suit)


@pytest.fixture(scope="class")
def players():
    players = []
    players.append(Player(0, "p1"))
    players.append(Player(1, "p2"))
    players.append(Player(2, "p3"))
    players.append(Player(3, "p4"))
    return players


@pytest.mark.usefixtures("deck", "players")
class TestDeckClass:
    # deal cards to players
    def test_deal(self, deck, players):
        deck.deal(5, players)

        # deck should have 32 cards (52 - 5*4)
        assert len(deck.cards) == 32

        # each player should have 5 cards
        for player in players:
            assert len(player.hand.cards) == 5

    # return cards from a player to deck
    def test_return_cards(self, deck, players):
        deck.return_cards(players[0].hand)

        # deck should have 37 cards (32 + 5)
        assert len(deck.cards) == 37

        # player should have 0 cards
        assert len(players[0].hand.cards) == 0
