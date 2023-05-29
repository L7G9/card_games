"""Contains class for a group of cards.

Classes:

    CardGroup

Typical usage examples:

    hand = CardGroup("My hand of cards")

    hand.cards.append(Card(Value.ACE, Suit.SPADES))

    hand.cards.append(Card(Value.QUEEN, Suit.HEARTS))

    hand.shuffle()

    print(hand.description())
"""

from random import shuffle

from model.card_game.card import Card


class CardGroup:
    """Class to represent a group cards.

    The is a generic structure that could be the main deck that cards are
    dealt from, a player's hand or the discard pile.

    Attributes:
        name: A string describing this card group.
        cards: A list of Card instances.
    """

    def __init__(self, name: str):
        """Initializes instance.

        Args:
            name: A string to set the name of card group.
        """
        self.name = name
        self.cards: list[Card] = []

    def description(self) -> str:
        """Returns a text description of the CardGroup.

        Returns:
            A string describing the CardGroup.
        """
        return "%s contains %d cards" % (self.name, len(self.cards))

    def shuffle(self):
        """Shuffles the Cards in this object into a random order."""
        shuffle(self.cards)
