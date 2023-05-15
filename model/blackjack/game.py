import random

from typing import Union

from model.card_game.suit import Suit
from model.card_game.card import Card
from model.card_game.deck import Deck

from model.blackjack.blackjack_value import BlackJackValue
from model.blackjack.player import Player
from model.blackjack.player_status import PlayerStatus
from model.blackjack.game_status import GameStatus
from model.blackjack.game_stats import GameStats
from model.blackjack.action_selector import ActionSelector


class Game:
    """Class to represent a Game of Blackjack."""

    def __init__(self, name: str):
        self.name = name
        self.deck = Deck("Deck", BlackJackValue, Suit)

        self.players: list[Player] = []
        self.status = GameStatus.DEALING
        self.active_player_index: int = 0
        self.game_stats: GameStats = None

    def deal(self) -> GameStatus:
        """"""
        self.deck.shuffle()
        for i in range(2):
            for player in self.players:
                player.add_card(self.deck.cards.pop())

        self.active_player_index = -1

        self.game_stats = GameStats(len(self.players))

        self.status = GameStatus.NEXT_PLAYER
        return self.status

    def next_player(self) -> GameStatus:
        self.active_player_index += 1

        if self.active_player_index == len(self.players):
            self.status = GameStatus.RESOLVING
        else:
            self.status = GameStatus.SENDING_ACTIONS
        return self.status

    def send_actions(self, player: Player) -> GameStatus:
        if player != self.players[self.active_player_index]:
            return self.status

        player.play()

        self.status = GameStatus.RECEIVING_ACTION
        return self.status

    def resolve_stick_action(
        self,
        player: Player,
    ) -> GameStatus:
        if player != self.players[self.active_player_index]:
            return self.status

        player.stick()
        self.game_stats.update(PlayerStatus.STICK)

        self.status = GameStatus.NEXT_PLAYER
        return self.status

    def resolve_twist_action(
        self,
        player: Player,
    ) -> Union[GameStatus, Card]:
        if player != self.players[self.active_player_index]:
            return self.status

        card = self.deck.cards.pop()
        if player.twist(card) == PlayerStatus.BUST:
            self.status = GameStatus.NEXT_PLAYER
            self.game_stats.update(PlayerStatus.BUST)
        else:
            self.status = GameStatus.SENDING_ACTIONS

        return self.status, card

    def resolve_game(self) -> Union[GameStatus, list[Player]]:
        winners = []
        best_total = 0

        for player in self.players:
            player.reveal_hand()
            if player.status == PlayerStatus.STICK:
                if player.best_total > best_total:
                    best_total = player.best_total
                    winners = [player]
                elif player.best_total == best_total:
                    winners.append(player)

        self.status = GameStatus.RESETTING
        return self.status, winners

    def reset_game(self, winners: list[Player]) -> GameStatus:
        if winners is not None:
            self.players = self.get_player_order(winners)

        for player in self.players:
            self.deck.return_cards(player.hand)
            player.reset()

        self.status = GameStatus.DEALING
        return self.status

    def get_player_order(self, winners: list[Player]) -> list[Player]:
        # check for no winners
        if not winners:
            return None

        # get index of one random winner
        winner = random.choice(winners)
        winner_index = self.players.index(winner)

        # create new list with chosen winner a the front
        players = []
        for index in range(winner_index, len(self.players)):
            players.append(self.players[index])
        for index in range(0, winner_index):
            players.append(self.players[index])

        return players
