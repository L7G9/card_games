from typing import Union

from model.card_game.suit import Suit
from model.card_game.card_group import CardGroup
from model.card_game.deck import Deck

from model.blackjack.blackjack_value import BlackJackValue
from model.blackjack.blackjack_player import BlackjackPlayer
from model.blackjack.player_status import PlayerStatus
from model.blackjack.blackjack_player_action import PlayerAction
from model.blackjack.game_status import GameStatus


class Game:
    """Class to represent a Game of Blackjack."""

    def __init__(self, name: str):
        self.name = name
        self.deck = Deck("Deck", BlackJackValue, Suit)
        self.players: list[BlackjackPlayer] = [
            BlackjackPlayer(0, "Liz", CardGroup("Liz's hand")),
            BlackjackPlayer(1, "Roger", CardGroup("Roger's hand")),
            BlackjackPlayer(2, "Noriko", CardGroup("Noriko's hand"))
        ]
        self.status = GameStatus.DEALING
        self.active_player: BlackjackPlayer = None

    def deal(self):
        """"""
        self.deck.shuffle()
        # self.deck.deal(2, self.players)
        for i in range(2):
            for player in self.players:
                player.add_card(self.deck.cards.pop())

        self.status = GameStatus.SENDING_ACTIONS
        self.active_player = 0

        return self.status

    def send_actions(self, player: BlackjackPlayer):
        if player != self.players[self.active_player]:
            return self.status

        player.receive_actions(
            [PlayerAction.STICK, PlayerAction.TWIST]
        )

        self.status = GameStatus.RECEIVING_ACTION

        return self.status

    def resolve_action(
        self,
        player: BlackjackPlayer,
        action: PlayerAction
    ):
        if player != self.players[self.active_player]:
            return self.status

        if action == PlayerAction.STICK:
            player.stick()
            self.active_player += 1
        elif action == PlayerAction.TWIST:
            if player.twist(self.deck.cards.pop()) == PlayerStatus.BUST:
                self.active_player += 1

        if self.active_player == len(self.players):
            self.status = GameStatus.RESOLVING
        else:
            self.status = GameStatus.SENDING_ACTIONS

        return self.status

    def resolve_game(self) -> Union[GameStatus, list[BlackjackPlayer]]:
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
