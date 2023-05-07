from card import Card
from suit import Suit
from value import Value


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

    def fill(self, number_of_decks, face_up, include_jokers):
        for deck in range(0, number_of_decks):

            if include_jokers:
                self.cards.append(Card(Value.Joker, Suit.Black, face_up))
                self.cards.append(Card(Value.Joker, Suit.Red, face_up))

            for value in Value:
                if value is not Value.Joker:
                    for suit in Suit:
                        if ((suit is not Suit.Black)
                            and (suit is not Suit.Red)):
                            self.cards.append(Card(value, suit, face_up))

    def shuffle(self):
        pass

    def description(self) -> str:
        return ("%s has %d cards" % (self.name, len(self.cards)))


if __name__ == '__main__':
    deck = CardGroup("Deck")
    deck.fill(2, True, True)
    print(deck.description())
    for card in deck.cards:
        print(card.description(True))
