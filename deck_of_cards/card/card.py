from suit import Suit
from value import Value

import functools

@functools.total_ordering
class Card:
    def __init__(self, value, suit, face_up=False):
        self.value = value
        self.suit = suit
        self.face_up = face_up


    def _is_valid_operand(self, other):
        return (hasattr(other, "value") and hasattr(other, "suit"))


    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.value == other.value) and (self.suit == other.suit))


    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented

        if self.value == other.value:
            return int(self.suit) < int(other.suit)
        else:
            return int(self.value) < int(other.value)


    def __str__(self):
        return self.description(False)


    def description(self, ignore_face_up):
        if ignore_face_up or self.face_up:
            return ("The %s of %s" % (self.value, self.suit))
        else:
            return "A facedown card"


    def flip(self):
        self.face_up = not self.face_up


if __name__ == '__main__':
    card1 = Card(Value.Ace, Suit.Spades)
    print(card1)
    card1.flip()
    print(card1)

    card2 = Card(Value.Ace, Suit.Hearts)
    print(card1 < card2)
    print(card1 > card2)
