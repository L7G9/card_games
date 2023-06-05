"""Contains class for a single card.

Classes:

    Card

Typical usage examples:

    card = Card(Value.ACE, Suit.SPADES, True)

    print(card)
"""

from model.card_game.suit import Suit
from model.card_game.value import Value


class Card:
    """Class to represent a playing card from a standard deck of cards.

    Attributes:
        value: The Value of the card Ace, Two, Three ... King
        suit: The Suit of the card Diamonds, Spades etc.
        face_up: A boolean set to True if the card is face up.
    """

    def __init__(self, value: Value, suit: Suit, face_up: bool = False):
        """Initializes instance.

        Args:
            value: A member from a Value enumeration.
            suit: A member from a Suit enumeration.
            face_up: A boolean set to True when the card is face up and
                visible to all players.  False by default.
        """
        self.value = value
        self.suit = suit
        self.face_up = face_up

    def __str__(self) -> str:
        """Return description of the Card, value & suit or face down card."""
        return self.description(False)

    def description(self, ignore_face_up: bool) -> str:
        """Returns a text description of the Card.

        Args:
            ignore_face_up: A boolean set to True to return the full
                description of the Card even if face_up is False.

        Returns:
            A string describing the Card.
        """
        if ignore_face_up or self.face_up:
            return "%s of %s" % (self.value, self.suit)
        else:
            return "Facedown card"
