from time import sleep
from os import system, name

from model.blackjack.game import Game
from model.blackjack.game_status import GameStatus
from model.blackjack.player import Player
from model.blackjack.action_selector import ActionSelector
from model.blackjack.player_status import PlayerStatus


class BlackjackTextController:
    """Controller for BlackJackGame and TextView."""

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

    def __init__(self):
        self.game = Game("Blackjack")

    def run(self):
        self.clear()
        print("Welcome to our game of Blackjack.")
        sleep(1)

        self.setup()

        continue_playing = True
        while continue_playing:
            self.play_game()

            winners = self.resolve_game()

            play_again = self.view.read("Play again? (y or n): ")
            continue_playing = play_again == 'y'
            if continue_playing:
                self.reset_game(winners)

    def setup(self):
        player_name = input("Enter your name: ")
        other_count = int(input("Enter number of other players (3 to 9): "))

        player = Player(0, player_name)
        self.game.players.append(player)
        for i in range(0, other_count):
            player = Player(i+1, self.names[i], ActionSelector())
            self.game.players.append(player)

        print("Our players are...")
        for player in self.game.players:
            print(player.name)

        sleep(2)
        self.clear()

    def play_game(self):
        print("Dealing.")
        self.game.deal()
        sleep(1)
        self.clear()

        while self.game.next_player() != GameStatus.RESOLVING:
            active_player = self.game.players[self.game.active_player_index]
            self.player_turn(active_player)

    def player_turn(self, active_player):
        while self.game.status != GameStatus.NEXT_PLAYER:
            print("It is %s's turn." % (active_player.name))
            self.game.send_actions(active_player)

            stick = False
            if active_player.action_selector:
                stick = active_player.action_selector.should_stick(
                    active_player.best_total,
                    self.game.game_stats
                )
            else:
                print(active_player.hand.description())
                for card in active_player.hand.cards:
                    print(card.description(True))
                chosen_action = input("Stick or Twist? (s or t): ")
                if chosen_action == 's':
                    stick = True
                elif chosen_action == 'f':
                    stick = False

            if stick:
                print("%s sticks." % (active_player.name))
                self.game.resolve_stick_action(active_player)
            else:
                print("%s twists." % (active_player.name))
                player_status, card = self.game.resolve_twist_action(
                    active_player
                )
                if active_player.action_selector is None:
                    print("And draws %s." % (card.description(True)))
                if active_player.status == PlayerStatus.BUST:
                    print("%s goes bust." % (active_player.name))

            sleep(2)
            self.clear()

    def resolve_game(self):
        print("Results.")

        games_status, winners = self.game.resolve_game()

        for player in self.game.players:
            print("%s reveals their cards..." % (player.name))
            for card in player.hand.cards:
                print(card.description(False))
            if player.status == PlayerStatus.BUST:
                print("Went bust.")
            else:
                print("Has a total of %d." % (player.best_total))
            sleep(1)

        if len(winners) == 0:
            print("No winners this round.")
        elif len(winners) == 1:
            print("The winner of this round is...")
            sleep(1)
            print(winners[0].name)
        else:
            print("The winners of this round are...")
            for player in winners:
                sleep(1)
                print(player.name)

        sleep(2)

        return winners

    def reset_game(self, winners):
        print("Resetting game.")
        self.game.reset_game(winners)
        print("Player order now is...")
        for player in self.game.players:
            self.view.write(player.name)

        sleep(2)
        self.clear()

    def clear(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')
