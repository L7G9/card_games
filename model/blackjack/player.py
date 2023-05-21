from typing import Set

from model.card_game import player
from model.card_game.card import Card

from model.blackjack.player_state import PlayerState
from model.blackjack.action_selector import ActionSelector
from model.blackjack.player_state_error import PlayerStateError


class Player(player.Player):
    """A Player in a game of Blackjack.

    Subclass of model.card_game.player.player with the functionality to for
    Blackjack.

    Attributes:
        state: A PlayerState set to the current state of the player in the
          game.
        totals: A set of integers containing all the totals that the cards in
          the player's hand could add up to.
        best_total: An integer equal to the best total of the cards in the
          player's hand.
        action_selector: An ActionSelector instance to choose if this player
        should stick or twist.  Set for computer controlled players.
    """
    def __init__(
        self,
        id: int,
        name: str,
        action_selector: ActionSelector = None
    ):
        """Initializes instance.

        Args:
            id: An unique integer id.
            name: A string for the player's name.
        """
        player.Player.__init__(self, id, name)
        self.action_selector = action_selector
        self.state = PlayerState.WAITING_TO_PLAY
        self.totals = {0}
        self.best_total = 0
        self.win_count = 0

    def user_controlled(self) -> bool:
        """Return True if player is user controlled."""
        return self.action_selector is None

    def app_controlled(self) -> bool:
        """Return True if player is app controlled with an ActionSelector."""
        return self.action_selector is not None

    def play(self) -> PlayerState:
        """Play - player start to or continues their turn.

        Can only be taken when player state is WAITING_TO_PLAY or
        DECIDING_ACTION.

        Returns:
            The new PlayerState, DECIDING_ACTION.

        Raises:
            PlayerStateError: Is state is not WAITING_TO_PLAY and is not
              DECIDING_ACTION.
        """
        if (self.state != PlayerState.WAITING_TO_PLAY
           and self.state != PlayerState.DECIDING_ACTION):
            raise PlayerStateError(
                self.state,
                [PlayerState.WAITING_TO_PLAY, PlayerState.DECIDING_ACTION]
            )

        self.state = PlayerState.DECIDING_ACTION

        return self.state

    def stick(self) -> PlayerState:
        """Stick action - player ends their go drawing no more cards.

        Can only be taken when player state is SELECTING_ACTION.

        Returns:
            The new PlayerState after taking this action, STICK.

        Raises:
            PlayerStateError: If state is not DECIDING_ACTION.
        """
        if self.state != PlayerState.DECIDING_ACTION:
            raise PlayerStateError(self.state, [PlayerState.DECIDING_ACTION])

        self.state = PlayerState.STICK

        return self.state

    def twist(self, card: Card) -> PlayerState:
        """Twist action - player receives a card.

        Can only be taken when player state is SELECTING_ACTION.
        Will increase the player's totals.
        The plyer will either be able to continue playing or go bust.

        Args:
            card: A Card instance to add to the player's hand.

        Returns:
            The new PlayerState after taking this action, either
              WAITING_FOR_ACTIONS or BUST.

        Raises:
            PlayerStateError: If state is not DECIDING_ACTION.
        """
        if self.state != PlayerState.DECIDING_ACTION:
            raise PlayerStateError(self.state, [PlayerState.DECIDING_ACTION])

        self.add_card(card)

        if self.best_total > 21:
            self.state = PlayerState.BUST
        else:
            self.state = PlayerState.DECIDING_ACTION

        return self.state

    def add_card(self, card: Card):
        """Add card to player's hand.

        Updates totals and best total to reflect the changes made by adding
        the card.

        Args:
            card: A Card instance to add to the player's hand.
        """
        self.hand.cards.append(card)
        self.totals = self.get_totals(self.totals, card)
        self.best_total = self.get_best_total(self.totals)

    def reset(self):
        """Reset player ready to start a new game of Blackjack."""
        self.hand.cards = []
        self.totals = {0}
        self.best_total = 0
        self.state = PlayerState.WAITING_TO_PLAY

    def reveal_hand(self):
        """Set all player's cards to face up."""
        for card in self.hand.cards:
            card.face_up = True

    def get_totals(self, totals: Set[int], card: Card) -> Set[int]:
        """Calculate possible totals when card is added to player's hand.

        Because aces are worth either 1 or 11, a player's hand can have
        multiple totals.

        Args:
            totals: A set of integers with the current totals in the player's
              hand.
            card: A Card instance whose value is to be added to the totals.

        Returns:
            A set of integers with the new totals in the player's hand.
        """
        new_totals = set()

        for total in totals:
            new_totals.add(total + card.value.game_value())
            if card.value.alt_game_value() is not None:
                new_totals.add(total + card.value.alt_game_value())

        return new_totals

    def get_best_total(self, totals: Set[int]) -> int:
        """Get best total from set of totals.

        The best total will be the highest total less then or equal to 21.
        When all totals are over 21, i.e. the player is bust, any of these can
        be considered the best total.

        Args:
            totals: A set of integers holding all possible totals in the
              player's hand.

        Returns:
            An integer with the best total.
        """
        best_total = 0
        for total in totals:
            none_set = best_total == 0
            best_is_bust = best_total > 21
            total_is_best = total > best_total and total <= 21

            if none_set or best_is_bust or total_is_best:
                best_total = total

        return best_total
