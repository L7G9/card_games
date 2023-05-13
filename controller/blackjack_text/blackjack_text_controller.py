from time import sleep

from model.card_game.card_group import CardGroup
from model.blackjack.game import Game
from model.blackjack.game_status import GameStatus
from model.blackjack.player import Player
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
            active_player = self.game.players[self.game.active_player_index]
            self.game.send_actions(active_player)

            self.view.write(active_player.hand.description())
            for card in active_player.hand.cards:
                self.view.write(card.description(True))

            chosen_action = self.view.read("Stick or Twist? (s or t): ")

            if chosen_action == 's':
                self.view.write("%s sticks." % (active_player.name))
                self.game.resolve_stick_action(active_player)

            elif chosen_action == 't':
                self.view.write("%s twists." % (active_player.name))
                self.game.resolve_twist_action(active_player)
                if active_player.status == PlayerStatus.BUST:
                    self.view.write("%s goes bust." % (active_player.name))

        # resolve game
        games_status, results = self.game.resolve_game()

        self.view.write("")
        self.view.write("Game complete.")
        self.view.write("")
        for player in self.game.players:
            self.view.write("%s has a total of %d with..." % (player.name, player.best_total))
            for card in player.hand.cards:
                self.view.write(card.description(False))
            self.view.write("")
            sleep(2)

        self.view.write("The winner(s) of this round is...")
        sleep(2)
        for player in results:
            self.view.write(player.name)
        self.view.write("")

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
        player = Player(
            3,
            name,
            CardGroup("%s's hand" % (name))
        )
        self.game.players.append(player)
