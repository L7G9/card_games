from typing import Set

from model.card_game.player import Player
from model.card_game.card import Card
from model.card_game.card_group import CardGroup

from model.blackjack.player_status import PlayerStatus
from model.blackjack.blackjack_player_action import PlayerAction


class BlackjackPlayer(Player):
    def __init__(
        self,
        id: int,
        name: str,
        hand: CardGroup
    ):
        Player.__init__(self, id, name, hand)
        self.available_actions = []
        self.status = PlayerStatus.WAITING_TO_PLAY
        self.totals = {0}
        self.best_total = 0

    def receive_actions(self, available_actions: list[PlayerAction]) -> PlayerStatus:
        waiting_to_play = self.status == PlayerStatus.WAITING_TO_PLAY
        waiting_for_actions = self.status == PlayerStatus.WAITING_FOR_ACTIONS
        waiting = waiting_to_play or waiting_for_actions
        if not waiting:
            return self.status

        self.available_actions = available_actions
        self.status = PlayerStatus.SELECTING_ACTION

        return self.status

    def stick(self) -> PlayerStatus:
        if self.status != PlayerStatus.SELECTING_ACTION:
            return self.status

        self.status = PlayerStatus.STICK

        return self.status

    def twist(self, card: Card) -> PlayerStatus:
        if self.status != PlayerStatus.SELECTING_ACTION:
            return self.status

        self.add_card(card)

        if self.best_total > 21:
            self.status = PlayerStatus.BUST
        else:
            self.status = PlayerStatus.WAITING_FOR_ACTIONS

        return self.status

    def add_card(self, card: Card):
        """Add card to player's hand and update totals."""
        self.hand.cards.append(card)
        self.totals = self.get_totals(self.totals, card)
        self.best_total = self.get_best_total(self.totals)

    def reset(self):
        """Remove cards from player's hand and clear totals."""
        self.hand.cards = []
        self.totals = {0}
        self.best_total = 0
        self.status = PlayerStatus.WAITING_TO_PLAY

    def reveal_hand(self):
        """Set all cards in player's hand to face up."""
        for card in self.hand.cards:
            card.face_up = True

    def get_totals(self, totals: Set[int], card: Card) -> Set[int]:
        """Get new set of totals when a card is added to this player's hand."""
        new_totals = set()

        for total in totals:
            new_totals.add(total + card.value.game_value())
            if card.value.game_value() == 1:
                new_totals.add(total + card.value.alt_game_value())

        return new_totals

    def get_best_total(self, totals: Set[int]) -> int:
        """Get best total from set of totals."""
        best_total = 0
        for total in totals:
            none_set = best_total == 0
            best_is_bust = best_total > 21
            total_is_best = total > best_total and total <= 21
            if none_set or best_is_bust or total_is_best:
                best_total = total

        return best_total
