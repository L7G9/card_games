from suit import Suit
from value import Value

import functools


@functools.total_ordering
class Card:
    """Class to represent a playing card from a standard deck of cards.

    Attributes:
        value: The Value of the card Ace, Two, Three ... King
        suit: The Suit of the card Diamonds, Spades etc.
        face_up: A boolean set to True if the card is face up.
    """
    def __init__(self, value: Value, suit: Suit, face_up: bool = False):
        self.value = value
        self.suit = suit
        self.face_up = face_up

    def _is_valid_operand(self, other) -> bool:
        return (hasattr(other, "value") and hasattr(other, "suit"))

    def __eq__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented

        return ((self.value == other.value) and (self.suit == other.suit))

    def __lt__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented

        if self.value == other.value:
            return int(self.suit) < int(other.suit)
        else:
            return int(self.value) < int(other.value)

    def __str__(self) -> str:
        return self.description(False)

    def description(self, ignore_face_up: bool) -> str:
        """Returns a text description of the card.

        Args:
            ignore_face_up: A boolean which when set to True makes this
            method print the full desciption of the card even if it is
            face_up is False.

        Returns:
            A string descibing the card.
        """
        if ignore_face_up or self.face_up:
            if self.value == Value.Joker:
                return ("%s %s" % (self.suit, self.value))
            else:
                return ("%s of %s" % (self.value, self.suit))
        else:
            return "Facedown card"

    def flip(self):
        """Flips the card over from face up to face down and vice versa."""
        self.face_up = not self.face_up
