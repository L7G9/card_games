from card import Card
from suit import Suit
from value import Value

from random import shuffle


class CardGroup:
    """Class to represent a group cards from a standard deck of cards.

    The is a generic structure that could be the main deck that cards are
    delt from, a player's hand or the discard pile.

    Attributes:
        cards: a list of Card objects.
        name: A name describing this card card group.
    """

    def __init__(self, name):
        self.cards = []
        self.name = name

    def fill(
        self,
        number_of_decks: int = 1,
        face_up: bool = False,
        include_jokers: bool = False,
    ):
        """Fill CardGroup with whole decks of Cards.

        Creates all the Card objects for all the Cards in one or more standard
        decks.

        Args:
            number_of_decks: An integer set to the number of whole decks of
            Cards to create.
            face_up: A boolean set to True to create all Cards face up.
            include_jokers: A boolean set to True to add Black and Red Jokers.
        """
        for deck in range(0, number_of_decks):
            if include_jokers:
                self.cards.append(Card(Value.Joker, Suit.Black, face_up))
                self.cards.append(Card(Value.Joker, Suit.Red, face_up))

            for value in Value:
                if value is not Value.Joker:
                    for suit in Suit:
                        if (suit is not Suit.Black) and (suit is not Suit.Red):
                            self.cards.append(Card(value, suit, face_up))

    def shuffle(self):
        """Shuffles the Cards in this object into a random order."""
        shuffle(self.cards)

    def description(self) -> str:
        """Returns a text description of the CardGroup.

        Returns:
            A string describing the CardGroup.
        """
        return "%s containing %d cards" % (self.name, len(self.cards))
