from card import Card

from random import shuffle


class CardGroup:
    """Class to represent a group cards.

    The is a generic structure that could be the main deck that cards are
    dealt from, a player's hand or the discard pile.

    Attributes:
        name: A name describing this card card group.
        cards: a list of Card objects.
    """
    def __init__(self, name: str):
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
