from typing import Union

from model.card_game.suit import Suit
from model.card_game.card_group import CardGroup
from model.card_game.deck import Deck

from model.blackjack.blackjack_value import BlackJackValue
from model.blackjack.blackjack_player import BlackjackPlayer as Player
from model.blackjack.blackjack_player_status import BlackjackPlayerStatus as PlayerStatus
from model.blackjack.blackjack_player_action import BlackjackPlayerAction as PlayerAction
from model.blackjack.blackjack_game_status import BlackjackGameStatus as GameStatus


class BlackjackGame:
    """Class to represent a Game of Blackjack."""

    def __init__(self, name: str):
        self.name = name
        self.deck = Deck("Deck", BlackJackValue, Suit)
        self.players: list[Player] = [
            Player(0, "Jane Doe", CardGroup("Jane's hand")),
            Player(1, "John Doe", CardGroup("John's hand"))
        ]
        self.status = GameStatus.DEALING
        self.active_player: Player = None

    def deal(self):
        """"""
        self.deck.shuffle()
        self.deck.deal(2, self.players)
        self.status = GameStatus.SENDING_ACTIONS
        self.active_player = 0

        return self.status

    def send_actions(self, player: Player):
        if player != self.players[self.active_player]:
            return

        player.receive_actions(
            [PlayerAction.Stick, PlayerAction.Twist]
        )

        self.status = GameStatus.RECIEVING_ACTIONS

        return self.status

    def resolve_action(
        self,
        player: Player,
        action: PlayerAction
    ):
        if player != self.players[self.active_player]:
            return

        if action == PlayerAction.STICK:
            player.stick()
            self.active_player += 1
        elif action == PlayerAction.TWIST:
            if player.twist(self.deck.cards.pop()) == PlayerStatus.Bust:
                self.active_player += 1

        if self.active_player == len(self.players):
            self.status = GameStatus.RESOLVING
        else:
            self.status = GameStatus.SENDING_ACTIONS

        return self.status

    def resolve_game(self) -> Union[GameStatus, list[Player]]:
        winners = []
        best_total = 0

        for player in self.players:
            if player.status == PlayerStatus.Stick:
                if player.stick_total > best_total:
                    best_total = player.stick_total
                    winners = [player]
                elif player.stick_total == best_total:
                    winners.append(player)

        self.status = GameStatus.RESETTING

        return self.status, winners

    def reset_game(self) -> GameStatus:
        for player in self.players:
            self.deck.return_cards(player.hand)
            player.status = PlayerStatus.WAITING_TO_PLAY

        self.status = GameStatus.DEALING

        return self.status
