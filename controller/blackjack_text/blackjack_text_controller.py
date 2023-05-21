from time import sleep

import inflect

from model.blackjack.game import Game
from model.blackjack.game_state import GameState
from model.blackjack.player import Player
from model.blackjack.action_selector import ActionSelector
from model.blackjack.player_state import PlayerState

from view.text_view.text_view import get_option
from view.text_view.text_view import clear_screen


class BlackjackTextController:
    """Controller for BlackJackGame and stdio."""

    names = [
        "Adam",
        "Betty",
        "Chris",
        "Denise",
        "Ethan",
        "Francesca",
        "Gregory",
        "Harriet",
        "Jake"
    ]

    SHORT_PAUSE = 1
    MEDIUM_PAUSE = 3
    LONG_PAUSE = 5

    def __init__(self):
        self.game = Game("Blackjack")

    def run(self):
        clear_screen()
        print("Welcome to our game of Blackjack.")
        sleep(self.SHORT_PAUSE)

        self.setup()

        continue_playing = True
        while continue_playing:
            self.play_game()

            winners = self.resolve_game()

            play_again = get_option("Play again? (y or n): ", ["y", "n"])
            continue_playing = play_again == "y"
            if continue_playing:
                self.reset_game(winners)
            else:
                clear_screen()
                print("Thankyou for playing.")
                sleep(self.SHORT_PAUSE)
                for player in self.game.players:
                    print("%s won %d games." % (player.name, player.win_count))

    def setup(self):
        player_name = input("Enter your name: ")
        app_player_count = int(
            get_option(
                "Enter number of opponent players (3 to 9): ",
                ["3", "4", "5", "6", "7", "8", "9"]
            )
        )

        user_player = Player(0, player_name)
        self.game.players.append(user_player)
        for i in range(0, app_player_count):
            app_player = Player(i+1, self.names[i], ActionSelector())
            self.game.players.append(app_player)

        print("Our players are...")
        for player in self.game.players:
            sleep(self.SHORT_PAUSE)
            print(player.name)

        sleep(self.MEDIUM_PAUSE)
        clear_screen()

    def play_game(self):
        print("Dealing.")
        self.game.deal()
        sleep(self.SHORT_PAUSE)
        clear_screen()

        while self.game.next_player() != GameState.RESOLVING_GAME:
            player = self.game.players[self.game.active_player_index]
            self.player_turn(player)

    def player_turn(self, player):
        while self.game.state != GameState.STARTING_PLAYER:
            print("It is %s's turn." % (player.name))
            self.game.start_turn(player)

            if player.user_controlled():
                self.user_player_actions(player)
            else:
                self.app_player_actions(player)

            sleep(self.MEDIUM_PAUSE)
            clear_screen()

    def user_player_actions(self, player):
        # display player's hand
        print(player.hand.description())
        for card in player.hand.cards:
            print(card.description(True))

        # get stick or twist option
        option = get_option("Stick or Twist? (s or t): ", ["s", "t"])
        sticking = option == "s"

        if sticking:
            # resolve stick action
            print("%s sticks." % (player.name))
            self.game.resolve_stick_action(player)
        else:
            # resolve twist action
            print("%s twists." % (player.name))
            game_state, card = self.game.resolve_twist_action(player)

            # feedback
            print("And draws %s." % (card.description(True)))
            if player.state == PlayerState.BUST:
                print("%s goes bust." % (player.name))

    def app_player_actions(self, player):
        # display count of cards in player's hand
        print(player.hand.description())

        # get stick or twist option
        sticking = player.action_selector.should_stick(
            player.best_total,
            self.game.game_stats
        )

        if sticking:
            # resolve stick action
            print("%s sticks." % (player.name))
            self.game.resolve_stick_action(player)
        else:
            # resolve twist action
            print("%s twists." % (player.name))
            game_state, card = self.game.resolve_twist_action(player)

            # feedback
            inflect_engine = inflect.engine()
            nth_card_drawn = inflect_engine.ordinal(
                len(player.hand.cards)-2
            )
            print("And draws %s card." % (nth_card_drawn))
            if player.state == PlayerState.BUST:
                print("%s goes bust." % (player.name))

    def resolve_game(self):
        print("Results.")

        games_state, winners = self.game.resolve_game()

        for player in self.game.players:
            print("%s reveals their cards..." % (player.name))
            for card in player.hand.cards:
                print(card.description(False))
            if player.state == PlayerState.BUST:
                print("Went bust.")
            else:
                print("Has a total of %d." % (player.best_total))
            sleep(self.MEDIUM_PAUSE)
            clear_screen()

        if len(winners) == 0:
            print("No winners this round.")
        elif len(winners) == 1:
            print("The winner of this round is...")
            sleep(self.SHORT_PAUSE)
            print(winners[0].name)
        else:
            print("The winners of this round are...")
            for player in winners:
                sleep(self.SHORT_PAUSE)
                print(player.name)

        sleep(self.LONG_PAUSE)
        clear_screen()

        return winners

    def reset_game(self, winners):
        print("Resetting game.")
        self.game.reset_game(winners)
        print("Player order now is...")
        for player in self.game.players:
            sleep(self.SHORT_PAUSE)
            print(player.name)

        sleep(self.LONG_PAUSE)
        clear_screen()
