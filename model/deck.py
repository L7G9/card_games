from model.value import Value
from model.suit import Suit
from model.card import Card
from model.card_group import CardGroup
from model.player import Player


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

if __name__ == '__main__':
    deck = Deck("Deck", Value, Suit)
    deck.shuffle()
    print(deck.description())
    for card in deck.cards:
        print(card.description(True))

    players = [
        Player(1, "John", CardGroup("John's hand")),
        Player(2, "Jane", CardGroup("Jane's hand")),
        Player(3, "Jack", CardGroup("Jack's hand")),
    ]

    deck.deal(5, players)
    for player in players:
        print(player.hand.description())
        for card in player.hand.cards:
            print(card.description(True))

    for player in players:
        deck.return_cards(player.hand)

    print(deck.description())
    for player in players:
        print(player.hand.description())
