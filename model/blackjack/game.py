from typing import Union

from model.card_game.suit import Suit
from model.card_game.card_group import CardGroup
from model.card_game.deck import Deck

from model.blackjack.blackjack_value import BlackJackValue
from model.blackjack.player import Player
from model.blackjack.player_status import PlayerStatus
from model.blackjack.game_status import GameStatus


class Game:
    """Class to represent a Game of Blackjack."""

    def __init__(self, name: str):
        self.name = name
        self.deck = Deck("Deck", BlackJackValue, Suit)
        self.players: list[Player] = [
            Player(0, "Liz"),
            Player(1, "Roger"),
            Player(2, "Noriko")
        ]
        self.status = GameStatus.DEALING
        self.active_player_index: int = 0

    def deal(self):
        """"""
        self.deck.shuffle()
        for i in range(2):
            for player in self.players:
                player.add_card(self.deck.cards.pop())

        self.status = GameStatus.SENDING_ACTIONS
        self.active_player_index = 0

        return self.status

    def send_actions(self, player: Player):
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
        self.active_player_index += 1

        if self.active_player_index == len(self.players):
            self.status = GameStatus.RESOLVING
        else:
            self.status = GameStatus.SENDING_ACTIONS

        return self.status

    def resolve_twist_action(
        self,
        player: Player,
    ) -> GameStatus:
        if player != self.players[self.active_player_index]:
            return self.status

        if player.twist(self.deck.cards.pop()) == PlayerStatus.BUST:
            self.active_player_index += 1

        if self.active_player_index == len(self.players):
            self.status = GameStatus.RESOLVING
        else:
            self.status = GameStatus.SENDING_ACTIONS

        return self.status

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

    def reset_game(self) -> GameStatus:
        for player in self.players:
            self.deck.return_cards(player.hand)
            player.reset()

        self.status = GameStatus.DEALING

        return self.status
