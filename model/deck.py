from value import Value
from suit import Suit
from card import Card
from card_group import CardGroup


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
        suits: Suit,
        include_jokers: bool = False,
    ):
        """Fill CardGroup with a whole deck of Cards.

        Creates all the Card objects for one standard deck of cards.

        Args:
            values: An Enumeration of the card values in the deck.
            suits: An Enumeration of the card suits in the deck.
            include_jokers: A boolean set to True to add Black and Red Jokers.
        """
        if include_jokers:
            self.cards.append(Card(values.Joker, Suit.Black))
            self.cards.append(Card(values.Joker, Suit.Red))

        for value in values:
            if value is not values.Joker:
                for suit in suits:
                    if (suit is not suits.Black) and (suit is not suits.Red):
                        self.cards.append(Card(value, suit))

    def deal(self, number_of_cards: int, card_groups: list[CardGroup]):
        """Deal Cards from this Deck.

        Removes cards from the top of this Deck and adds them to the end
        CardGroup one by one until each CardGroup have the same number of
        Cards.

        Args:
            number_of_cards: An int for the number of card each CardGroup
            should receive.
            card_groups: A list of CardGroups to receive the cards.
        """
        for card_count in range(0, number_of_cards):
            for card_group in card_groups:
                card_group.cards.append(self.cards.pop())


if __name__ == '__main__':
    deck = Deck("Deck", Value, Suit)
    deck.shuffle()
    print(deck.description())
    for card in deck.cards:
        print(card.description(True))

    card_groups = [
        CardGroup("Player 1"),
        CardGroup("Player 2"),
        CardGroup("Player 3")
    ]

    deck.deal(5, card_groups)
    for card_group in card_groups:
        print(card_group.description())
        for card in card_group.cards:
            print(card.description(True))
