from card import Card
from suit import Suit
from value import Value

from random import shuffle


class CardGroup:
    """Class to represent a group cards.

    The is a generic structure that could be the main deck that cards are
    dealt from, a player's hand or the discard pile.

    Attributes:
        cards: a list of Card objects.
        name: A name describing this card card group.
    """

    def __init__(self, name):
        self.cards = []
        self.name = name

    def shuffle(self):
        """Shuffles the Cards in this object into a random order."""
        shuffle(self.cards)

    def description(self) -> str:
        """Returns a text description of the CardGroup.

        Returns:
            A string describing the CardGroup.
        """
        return "%s contains %d cards" % (self.name, len(self.cards))
