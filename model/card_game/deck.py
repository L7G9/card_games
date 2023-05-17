from model.card_game.value import Value
from model.card_game.suit import Suit
from model.card_game.card import Card
from model.card_game.card_group import CardGroup
from model.card_game.player import Player


class Deck(CardGroup):
    """Class to represent a standard deck of cards.

    A deck of cards with no jokers.

    Attributes:
        cards: A list of Card objects.
        name: A name describing this card card group.
    """
    def __init__(self, name: str, values: Value, suits: Suit):
        CardGroup.__init__(self, name)
        self.add_deck(values, suits)

    def add_deck(
        self,
        values: Value,
        suits: Suit
    ):
        """Fill CardGroup with a whole deck of Cards.

        Creates all the Card objects for one standard deck of cards.

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
            number_of_cards: An int for the number of card each CardGroup
            should receive.
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
