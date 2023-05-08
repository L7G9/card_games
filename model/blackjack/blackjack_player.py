from player import Player
from card_group import CardGroup
from blackjack_game import BlackjackGame as Game
from blackjack_player_status import BlackjackPlayerStatus as PlayerStatus
from blackjack_player_actions import BlackjackPlayerActions as PlayerActions


class BlackjackPlayer(Player):
    def __init__(
        self,
        id: int,
        name: str,
        game: Game,
        hand: CardGroup
    ):
        Player.__init__(self, id, name, hand)
        self.game = game
        self.available_actions = []
        self.status = PlayerStatus.WaitingToPlay

    def receive_actions(self, available_actions: PlayerActions):
        waiting_to_play = self.status == PlayerStatus.WaitingToPlay
        waiting_for_actions = self.status == PlayerStatus.WaitingForActions

        if not waiting_to_play or not waiting_for_actions:
            return self.status

        self.available_actions = available_actions
        self.status = PlayerStatus.SelectingAction

        return self.status

    def stick(self) -> PlayerStatus:
        if self.status != PlayerStatus.SelectingAction:
            return self.status

        self.status = PlayerStatus.Stick
        total_values = self.get_total_values()
        self.stick_total = self.get_best_total(total_values)

        return self.status

    def twist(self) -> PlayerStatus:
        if self.status != PlayerStatus.SelectingAction:
            return self.status

        self.hand.cards.append(self.game.deck.cards.pop())
        total_values = self.get_total_values()
        best_total = self.get_best_total(total_values)

        if best_total > 21:
            self.status = PlayerStatus.Bust
        else:
            self.status = PlayerStatus.WaitingForActions

        return self.status

    def get_total_values(self) -> list[int]:
        """Get all possible combinations of the total values of all the cards
        in the player's hand.

        Takes into account aces can be worth 1 or 11.

        Returns:
            A list of integers containing the possible total values this
            player's hand could be.
        """
        totals = []
        for card in self.hand.cards:
            if card.value.game_value() == 1:
                if len(totals) == 0:
                    totals.append(card.value.game_value())
                    totals.append(card.value.alt_game_value())
                else:
                    current_totals_count = len(totals)-1
                    for index in range(0, current_totals_count):
                        totals.append(
                            totals[index]+card.value.alt_game_value()
                        )
                        totals[index] += card.value.game_value()
            else:
                if len(totals) == 0:
                    totals.append(card.value.game_value())
                else:
                    for index in range(0, len(totals)-1):
                        totals[index] += card.value.game_value()

        return totals

    def get_best_total(self, totals: list[int]) -> int:
        """Returns the best total value from list of all possible total card
        values in the Player's hand.

        The best value will be the the largest total value equal to or under
        21.  If there are none under 21, any value over 21 is the best value.

        Returns:
            An integer equal to the best total value from the card values in
            the Player's hand.
        """
        best_total = None

        for total in totals:
            if best_total is None:
                best_total = total
            elif best_total > 21 and total <= 21:
                best_total = total
            elif best_total < total and total <= 21:
                best_total = total

        return best_total
