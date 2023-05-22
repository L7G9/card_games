import pytest

from model.card_game.card import Card
from model.card_game.suit import Suit

from model.blackjack.game import Game
from model.blackjack.game_state import GameState
from model.blackjack.player import Player
from model.blackjack.player_state import PlayerState
from model.blackjack.value import Value as Value
from model.blackjack.game_stats import GameStats


# a new game for testing start of game events
@pytest.fixture(scope="function")
def new_game():
    game = Game("New Test Game")
    game.players.append(Player(0, "Test Player 0"))
    game.players.append(Player(1, "Test Player 1"))
    game.players.append(Player(2, "Test Player 2"))
    game.players.append(Player(3, "Test Player 3"))
    return game


# player who twists then sticks
@pytest.fixture(scope="function")
def twist_and_stick_player():
    player = Player(0, "Test Player 0")
    player.add_card(Card(Value.TWO, Suit.CLUBS))
    player.add_card(Card(Value.THREE, Suit.CLUBS))
    return player


# player who twists and goes bust
@pytest.fixture(scope="function")
def twist_and_bust_player():
    player = Player(1, "Test Player 1")
    player.add_card(Card(Value.QUEEN, Suit.CLUBS))
    player.add_card(Card(Value.KING, Suit.CLUBS))
    return player


# player with the winning hand
@pytest.fixture(scope="function")
def winner_player():
    player = Player(2, "Test Player 2")
    player.add_card(Card(Value.ACE, Suit.CLUBS))
    player.add_card(Card(Value.TEN, Suit.CLUBS))
    player.state = PlayerState.STICK
    return player


# player with a non-winning hand
@pytest.fixture(scope="function")
def other_player():
    player = Player(2, "Test Player 3")
    player.add_card(Card(Value.EIGHT, Suit.CLUBS))
    player.add_card(Card(Value.NINE, Suit.CLUBS))
    player.state = PlayerState.STICK
    return player


# an in progress game for testing player actions
@pytest.fixture(scope="function")
def in_progress_game(
    twist_and_stick_player,
    twist_and_bust_player,
    winner_player,
    other_player
):
    game = Game("In Progress Test Game")
    game.deck.cards.clear()

    game.players.append(twist_and_stick_player)
    game.players.append(twist_and_bust_player)
    game.players.append(winner_player)
    game.players.append(other_player)

    game.active_player_index = -1
    game.game_stats = GameStats(len(game.players))
    game.state = GameState.GETTING_NEXT_PLAYER

    return game


# a finished game for testing end of game actions
@pytest.fixture(scope="function")
def finished_game(
    twist_and_stick_player,
    twist_and_bust_player,
    winner_player,
    other_player
):
    game = Game("In Progress Test Game")
    game.deck.cards.clear()

    twist_and_stick_player.add_card(Card(Value.FOUR, Suit.CLUBS))
    twist_and_stick_player.state = PlayerState.STICK
    game.players.append(twist_and_stick_player)

    twist_and_bust_player.add_card(Card(Value.KING, Suit.CLUBS))
    twist_and_stick_player.state = PlayerState.BUST
    game.players.append(twist_and_bust_player)

    game.players.append(winner_player)
    game.players.append(other_player)

    game.active_player_index = 3
    game.game_stats = GameStats(len(game.players))
    game.state = GameState.GETTING_NEXT_PLAYER

    return game


class TestGameClass:
    # deal cards to players
    def test_deal(self, new_game):
        assert new_game.deal() == GameState.GETTING_NEXT_PLAYER
        assert len(new_game.deck.cards) == (52 - 8)
        for player in new_game.players:
            assert len(player.hand.cards) == 2

    # get next player after dealing
    def test_next_player_after_deal(self, new_game):
        new_game.state = GameState.GETTING_NEXT_PLAYER
        assert new_game.next_player() == GameState.STARTING_PLAYER_TURN
        assert new_game.active_player_index == 0

    # player starts their turn
    def test_start_turn(self, new_game):
        new_game.deal()
        new_game.next_player()
        player = new_game.players[new_game.active_player_index]
        assert (
            new_game.start_turn(player)
            == GameState.WAITING_FOR_PLAYER
        )
        assert player.state == PlayerState.DECIDING_ACTION

    # player twists and does not so bust
    def test_resolve_twist_action_not_bust(
            self,
            in_progress_game,
            twist_and_stick_player
    ):
        # set up deck
        card_from_deck = Card(Value.FOUR, Suit.CLUBS)
        in_progress_game.deck.cards.append(card_from_deck)

        # set game and player states
        in_progress_game.state = GameState.WAITING_FOR_PLAYER
        in_progress_game.active_player_index = 0
        twist_and_stick_player.state = PlayerState.DECIDING_ACTION

        # resolve twist action
        game_state, card = in_progress_game.resolve_twist_action(
            twist_and_stick_player
        )

        # check results
        assert game_state == GameState.STARTING_PLAYER_TURN
        assert card == card_from_deck
        assert in_progress_game.deck.cards == []

        assert twist_and_stick_player.state == PlayerState.DECIDING_ACTION
        assert card_from_deck in twist_and_stick_player.hand.cards
        assert twist_and_stick_player.best_total == (2 + 3 + 4)

    # player sticks
    def test_resolve_stick_action(
        self,
        in_progress_game,
        twist_and_stick_player
    ):
        # set game and player states
        in_progress_game.state = GameState.WAITING_FOR_PLAYER
        in_progress_game.active_player_index = 0
        twist_and_stick_player.state = PlayerState.DECIDING_ACTION

        # resolve twist action
        game_state = in_progress_game.resolve_stick_action(
            twist_and_stick_player
        )

        # check results
        assert game_state == GameState.GETTING_NEXT_PLAYER
        assert twist_and_stick_player.state == PlayerState.STICK

    # player twists and goes bust
    def test_resolve_twist_action_bust(
        self, in_progress_game,
        twist_and_bust_player
    ):
        # set up deck
        card_from_deck = Card(Value.JACK, Suit.CLUBS)
        in_progress_game.deck.cards.append(card_from_deck)

        # set game and player state'
        in_progress_game.state = GameState.WAITING_FOR_PLAYER
        in_progress_game.active_player_index = 1
        twist_and_bust_player.state = PlayerState.DECIDING_ACTION

        # resolve twist action
        game_state, card = in_progress_game.resolve_twist_action(
            twist_and_bust_player
        )

        # check results
        assert game_state == GameState.GETTING_NEXT_PLAYER
        assert card == card_from_deck
        assert in_progress_game.deck.cards == []

        assert twist_and_bust_player.state == PlayerState.BUST
        assert card_from_deck in twist_and_bust_player.hand.cards
        assert twist_and_bust_player.best_total == (10 + 10 + 10)

    # get next player after all players have finished
    def test_next_player_no_more_players(self, finished_game):
        assert finished_game.next_player() == GameState.RESOLVING_GAME

    # resolve game ready to report winners
    def test_resolve_game(self, finished_game, winner_player):
        finished_game.next_player()
        game_state, winners = finished_game.resolve_game()
        assert game_state == GameState.RESETTING_GAME
        assert winners[0] == winner_player

    # get new playing order for players based on winner
    def test_get_player_order(self, finished_game):
        winners = finished_game.get_winners()
        correct_order = [
            finished_game.players[2],
            finished_game.players[3],
            finished_game.players[0],
            finished_game.players[1]
        ]
        assert finished_game.get_player_order(winners) == correct_order

    # reset game ready to deal again
    def test_reset_game(self, finished_game):
        winners = finished_game.get_winners()
        finished_game.state = GameState.RESETTING_GAME
        assert finished_game.reset_game(winners) == GameState.DEALING
        assert len(finished_game.deck.cards) == (3 + 3 + 2 + 2)
