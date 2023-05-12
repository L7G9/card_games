from model.card_game import card_group
from model.blackjack import blackjack_game
from model.blackjack import game_status
from model.blackjack import blackjack_player
from model.blackjack import blackjack_player_action
from model.blackjack import blackjack_player_status

from view.text_view import text_view as view


class BlackjackTextController:
    """Controller for BlackJackGame and TextView."""
    def __init__(self):
        self.game = blackjack_game.BlackjackGame("Blackjack")
        self.view = view.TextView()

    def run(self):
        self.view.write_line("Welcome to Blackjack.")
        self.setup_user_player()

        continue_playing = True
        while continue_playing is True:

            # setup game
            self.game.deal()

            # play game
            while self.game.status != game_status.GameStatus.RESOLVING:
                active_player = self.game.players[self.game.active_player]
                self.game.send_actions(active_player)

                self.view.write_line(active_player.hand.description())
                for card in active_player.hand.cards:
                    self.view.write_line(card.description(True))

                chosen_action = self.view.read("Stick or Twist? (s or t): ")

                if chosen_action == 's':
                    self.view.write_line("%s sticks." % (active_player.name))
                    self.game.resolve_action(
                        active_player,
                        blackjack_player_action.PlayerAction.STICK
                    )

                elif chosen_action == 't':
                    self.view.write_line("%s twists." % (active_player.name))
                    self.game.resolve_action(
                        active_player,
                        blackjack_player_action.PlayerAction.TWIST
                    )
                    if active_player.status == blackjack_player_status.PlayerStatus.BUST:
                        self.view.write_line("%s goes bust." % (active_player.name))

            # resolve game
            games_status, results = self.game.resolve_game()
            self.view.write_line("The winner(s) of this round is...")
            for name in results:
                self.view.write_line(name)

            # reset game
            play_again = self.view.read("Play again? (y or n): ")
            continue_playing = play_again == 'y'
            if continue_playing:
                self.game.reset_game()

    def setup_user_player(self):
        name = self.view.read("Enter name: ")
        player = blackjack_player.BlackjackPlayer(
            3,
            name,
            card_group.CardGroup("%s's hand" % (name))
        )
        self.game.players.append(player)



    # set up game

    # run game
    # get restart
    # restart game
