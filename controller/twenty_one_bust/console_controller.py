"""MVC Controller class for the twenty_one_bust model and text view.

Classes:

    ConsoleController

Typical usage examples:

    controller = ConsoleController()

    controller.run()
"""

from time import sleep

import inflect

from model.twenty_one_bust.action_selector import ActionSelector
from model.twenty_one_bust.game import Game
from model.twenty_one_bust.game_state import GameState
from model.twenty_one_bust.player import Player
from model.twenty_one_bust.player_state import PlayerState
from view.text_view.text_view import clear_screen, get_option


class ConsoleController:
    """Controller for model.twenty_one_bust.game.Game and console.

    Coordinates model and text view (print, input, get_option & clear_screen)
    to run a game of 21 Bust for the user.

    Attributes:
        game: A Game instance of our 21 Bust game.
    """

    names = [
        "Adam",
        "Betty",
        "Chris",
        "Denise",
        "Ethan",
        "Francesca",
        "Gregory",
        "Harriet",
        "Jake",
    ]

    SHORT_PAUSE = 1
    MEDIUM_PAUSE = 3
    LONG_PAUSE = 5

    def __init__(self):
        """Initializes instance."""
        self.game = Game("21 Bust")

    def run(self):
        """Enters main loop for the game of 21 Bust.

        Performs initiaL Setup, plays game then prompts user to play again.
        Then depending on their response, resets the game and repeats or
        prints each player's win count.
        """
        clear_screen()
        print("Welcome to our game of 21 Bust.")
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
                sorted_players = sorted(
                    self.game.players,
                    reverse=True,
                    key=lambda player: player.win_count,
                )
                for player in sorted_players:
                    print("%s won %d games." % (player.name, player.win_count))

    def setup(self):
        """Perform initial setup of game.

        Asks user for their name and how many players they would like to play
        against.  Creates player instances for each of those and provides
        feedback.
        """
        player_name = input("Enter your name: ")
        app_player_count = int(
            get_option(
                "Enter number of opponent players (3 to 9): ",
                ["3", "4", "5", "6", "7", "8", "9"],
            )
        )

        user_player = Player(0, player_name)
        self.game.players.append(user_player)
        for i in range(0, app_player_count):
            app_player = Player(i + 1, self.names[i], ActionSelector())
            self.game.players.append(app_player)

        print("Our players are...")
        for player in self.game.players:
            sleep(self.SHORT_PAUSE)
            print(player.name)

        first_player = self.game.randomize_first_player()
        print("%s has been selected to go first." % (first_player.name))
        sleep(self.MEDIUM_PAUSE)
        clear_screen()

    def play_game(self):
        """Plays the game.

        Deals cards and loops through each player until each had completed
        their turn.
        """
        print("Dealing.")
        self.game.deal()
        sleep(self.SHORT_PAUSE)
        clear_screen()

        while self.game.next_player() != GameState.RESOLVING_GAME:
            player = self.game.players[self.game.active_player_index]
            self.player_turn(player)

    def player_turn(self, player):
        """Process a player's turn.

        Loops through player's actions until their turn is complete.

        Args:
            player: The Player instance who's turn it is.
        """
        while self.game.state != GameState.GETTING_NEXT_PLAYER:
            print("It is %s's turn." % (player.name))
            self.game.start_turn(player)

            if player.user_controlled():
                self.user_player_actions(player)
            else:
                self.app_player_actions(player)

            sleep(self.MEDIUM_PAUSE)
            clear_screen()

    def user_player_actions(self, player):
        """Process a user controlled player's action.

        Prompts user to stick to twist, updates game instance with their
        choice and provides feedback.

        Args:
            player: The Player instance who's turn it is.
        """
        # TODO: rename to user_player_action
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
        """Process an app controlled player's action.

        Uses players' action selector instance to stick to twist, updates game
        instance with their choice and provides feedback.

        Args:
            player: The Player instance who's turn it is.
        """
        # TODO: rename to ap_player_action
        # display count of cards in player's hand
        print(player.hand.description())

        # get stick or twist option
        sticking = player.action_selector.should_stick(
            player.best_total, self.game.game_stats
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
            nth_card_drawn = inflect_engine.ordinal(len(player.hand.cards) - 2)
            print("And draws %s card." % (nth_card_drawn))
            if player.state == PlayerState.BUST:
                print("%s goes bust." % (player.name))

    def resolve_game(self):
        """Provides feedback to user on the results of the game.

        Updates the game instance now all players have had their turn.
        Displays the contents of each players hand and the total when
        sicking or if they went bust, then displays who won this game.
        """
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

        sleep(self.MEDIUM_PAUSE)
        clear_screen()

        return winners

    def reset_game(self, winners):
        """Prepare game to play again.

        Update the game instance ready to play again.  Display the new order
        in which the players will take their turn.

        Args:
            winners: A list of player instances who won the last game.
        """
        print("Resetting game.")
        self.game.reset_game(winners)
        print("Player order now is...")
        for player in self.game.players:
            sleep(self.SHORT_PAUSE)
            print(player.name)

        sleep(self.LONG_PAUSE)
        clear_screen()
