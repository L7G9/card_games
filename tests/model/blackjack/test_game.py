import pytest

from model.card_game.card import Card
from model.card_game.suit import Suit

from model.blackjack.game import Game
from model.blackjack.game_status import GameStatus
from model.blackjack.player import Player
from model.blackjack.player_status import PlayerStatus
from model.blackjack.blackjack_value import BlackJackValue as Value
from model.blackjack.game_stats import GameStats


# a new game for testing start of game events
@pytest.fixture(scope="class")
def new_game():
    game = Game("New Test Game")
    game.players.append(Player(0, "Test Player 1"))
    game.players.append(Player(1, "Test Player 2"))
    game.players.append(Player(2, "Test Player 3"))
    game.players.append(Player(3, "Test Player 4"))
    return game


# an in progress game for testing player actions and end of game events
@pytest.fixture(scope="class")
def in_progress_game():
    game = Game("In Progress Test Game")
    game.deck.cards.clear()

    # player for twists then sticks
    player0 = Player(0, "Test Player 0 - stick 9")
    game.players.append(player0)

    # player who twists and goes bust
    player1 = Player(1, "Test Player 1 - bust 30")
    game.players.append(player1)

    # player with winning hand
    player2 = Player(2, "Test Player 2 - winner 21")
    player2.add_card(Card(Value.ACE, Suit.CLUBS))
    player2.add_card(Card(Value.TEN, Suit.CLUBS))
    player2.play()
    player2.stick()
    game.players.append(player2)

    # player with a non-winning hand
    player3 = Player(3, "Test Player 3 - stick 17")
    player3.add_card(Card(Value.EIGHT, Suit.CLUBS))
    player3.add_card(Card(Value.NINE, Suit.CLUBS))
    player3.play()
    player3.stick()
    game.players.append(player3)

    game.active_player_index = -1
    game.game_stats = GameStats(len(game.players))
    game.status = GameStatus.STARTING_PLAYER

    return game


@pytest.mark.usefixtures("new_game", "in_progress_game")
class TestGameClass:
    # deal cards to players
    def test_deal(self, new_game):
        assert new_game.deal() == GameStatus.STARTING_PLAYER
        assert len(new_game.deck.cards) == (52 - 8)
        for player in new_game.players:
            assert len(player.hand.cards) == 2

    # get next player after dealing
    def test_next_player_after_deal(self, new_game):
        assert new_game.next_player() == GameStatus.GETTING_PLAYER_ACTION

    # player starts their turn
    def test_start_turn(self, new_game):
        player = new_game.players[new_game.active_player_index]
        assert (
            new_game.start_turn(player)
            == GameStatus.RESOLVING_PLAYER_ACTION
        )
        assert player.status == PlayerStatus.DECIDING_ACTION

    # player twists and does not so bust
    def test_resolve_twist_action_not_bust(self, in_progress_game):
        # set up deck
        card_from_deck = Card(Value.FOUR, Suit.CLUBS)
        in_progress_game.deck.cards.append(card_from_deck)

        # set up players hand
        player = in_progress_game.players[0]
        player.add_card(Card(Value.TWO, Suit.CLUBS))
        player.add_card(Card(Value.THREE, Suit.CLUBS))

        # set game and player status'
        in_progress_game.status = GameStatus.RESOLVING_PLAYER_ACTION
        in_progress_game.active_player_index = 0
        player.status = PlayerStatus.DECIDING_ACTION

        # resolve twist action
        game_status, card = in_progress_game.resolve_twist_action(player)

        # check results
        assert game_status == GameStatus.GETTING_PLAYER_ACTION
        assert card == card_from_deck
        assert in_progress_game.deck.cards == []

        assert player.status == PlayerStatus.DECIDING_ACTION
        assert card_from_deck in player.hand.cards
        assert player.best_total == 9

    # player sticks
    def test_resolve_stick_action(self, in_progress_game):
        # Set up done be previous test
        player = in_progress_game.players[0]

        # resolve twist action
        game_status = in_progress_game.resolve_stick_action(player)

        # check results
        assert game_status == GameStatus.STARTING_PLAYER
        assert player.status == PlayerStatus.STICK

    # player twists and goes bust
    def test_resolve_twist_action_bust(self, in_progress_game):
        # set up deck
        card_from_deck = Card(Value.JACK, Suit.CLUBS)
        in_progress_game.deck.cards.append(card_from_deck)

        # set up players hand
        player = in_progress_game.players[1]
        player.add_card(Card(Value.QUEEN, Suit.CLUBS))
        player.add_card(Card(Value.KING, Suit.CLUBS))

        # set game and player status'
        in_progress_game.status = GameStatus.RESOLVING_PLAYER_ACTION
        in_progress_game.active_player_index = 1
        player.status = PlayerStatus.DECIDING_ACTION

        # resolve twist action
        game_status, card = in_progress_game.resolve_twist_action(player)

        # check results
        assert game_status == GameStatus.STARTING_PLAYER
        assert card == card_from_deck
        assert in_progress_game.deck.cards == []

        assert player.status == PlayerStatus.BUST
        assert card_from_deck in player.hand.cards
        assert player.best_total == 30

    # get next player after all players have finished
    def test_next_player_no_more_players(self, in_progress_game):
        in_progress_game.active_player_index = 3
        assert in_progress_game.next_player() == GameStatus.RESOLVING_GAME

    # resolve game ready to report winners
    def test_resolve_game(self, in_progress_game):
        """Test that winner is found when game is resolved."""
        game_status, winners = in_progress_game.resolve_game()
        assert game_status == GameStatus.RESETTING_GAME
        assert winners[0] == in_progress_game.players[2]

    # get new playing order for players based on winner
    def test_get_player_order(self, in_progress_game):
        winners = in_progress_game.get_winners()
        correct_order = [
            in_progress_game.players[2],
            in_progress_game.players[3],
            in_progress_game.players[0],
            in_progress_game.players[1]
        ]
        assert in_progress_game.get_player_order(winners) == correct_order

    # reset game ready to deal again
    def test_reset_game(self, in_progress_game):
        winners = in_progress_game.get_winners()
        assert in_progress_game.reset_game(winners) == GameStatus.DEALING
        assert len(in_progress_game.deck.cards) == (3 + 3 + 2 + 2)
