"""Contains class for a card of cards.

Classes:

    Deck

Typical usage examples:

    deck = Deck("Deck", Value, Suit)

    players = [Player(1, "John"), Player(2, "Jane")]

    deck.deal(5, players)

    deck.return_cards(players[0].cards)
"""

from model.card_game.card import Card
from model.card_game.card_group import CardGroup
from model.card_game.player import Player
from model.card_game.suit import Suit
from model.card_game.value import Value


class Deck(CardGroup):
    """Class to represent a standard deck of cards.

    A deck of cards with no jokers.

    Attributes:
        cards: A list of Card instances.
        name: A name describing this deck.
    """

    def __init__(self, name: str, values: Value, suits: Suit):
        """Initializes instance.

        Adds one standard set of 52 cards to this deck.

        Args:
            name: A string for the player's name.
            values: Value enumeration of card values.
            suits: Suit enumeration of card suits.
        """
        CardGroup.__init__(self, name)
        self.add_deck(values, suits)

    def add_deck(self, values: Value, suits: Suit):
        """Add deck of Cards.

        Creates all the Card objects for one standard deck of cards and adds
        it to this deck.  Can be used multiple times for larger deck sizes.

        Args:
            values: An Enumeration of the card values in the deck.
            suits: An Enumeration of the card suits in the deck.
        """
        for value in values:
            for suit in suits:
                self.cards.append(Card(value, suit))

    def deal(self, number_of_cards: int, players: list[Player]):
        """Deal Cards from this Deck.

        Removes cards from the top of this Deck and adds them to the end
        CardGroup one by one until each CardGroup have the same number of
        Cards.

        Args:
            number_of_cards: An integer equal to the number of cards each
                Player's hand should receive.
            players: A list of Players to receive the cards.
        """
        for card_count in range(0, number_of_cards):
            for player in players:
                player.hand.cards.append(self.cards.pop())

    def return_cards(self, card_group: CardGroup):
        """Returns Cards to Deck.

        Adds all the Cards in the CardGroup face down.
        Then removes the Cards from the CardGroup.

        Args:
            card_group: A CardGroup object to return the cards from.
        """
        for card in card_group.cards:
            card.face_up = False
            self.cards.append(card)
        card_group.cards = []
