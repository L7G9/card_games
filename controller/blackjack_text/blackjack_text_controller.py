from model.card_game.card_group import CardGroup
from model.blackjack.game import Game
from model.blackjack.game_status import GameStatus
from model.blackjack.blackjack_player import BlackjackPlayer
from model.blackjack.blackjack_player_action import PlayerAction
from model.blackjack.player_status import PlayerStatus

from view.text_view import text_view as view


class BlackjackTextController:
    """Controller for BlackJackGame and TextView."""
    def __init__(self):
        self.game = Game("Blackjack")
        self.view = view.TextView()

    def play_game(self):
        # setup game
        self.game.deal()

        # play game
        while self.game.status != GameStatus.RESOLVING:
            active_player = self.game.players[self.game.active_player]
            self.game.send_actions(active_player)

            self.view.write(active_player.hand.description())
            for card in active_player.hand.cards:
                self.view.write(card.description(True))

            chosen_action = self.view.read("Stick or Twist? (s or t): ")

            if chosen_action == 's':
                self.view.write("%s sticks." % (active_player.name))
                self.game.resolve_action(
                    active_player,
                    PlayerAction.STICK
                )

            elif chosen_action == 't':
                self.view.write("%s twists." % (active_player.name))
                self.game.resolve_action(
                    active_player,
                    PlayerAction.TWIST
                )
                if active_player.status == PlayerStatus.BUST:
                    self.view.write("%s goes bust." % (active_player.name))

        # resolve game
        games_status, results = self.game.resolve_game()
        self.view.write("The winner(s) of this round is...")
        for player in results:
            self.view.write(player.name)

    def run(self):
        self.view.write("Welcome to our game of Blackjack.")
        self.setup_user_player()

        continue_playing = True
        while continue_playing is True:

            self.play_game()

            # reset game
            play_again = self.view.read("Play again? (y or n): ")
            continue_playing = play_again == 'y'
            if continue_playing:
                self.game.reset_game()

    def setup_user_player(self):
        name = self.view.read("Enter name: ")
        player = BlackjackPlayer(
            3,
            name,
            CardGroup("%s's hand" % (name))
        )
        self.game.players.append(player)
