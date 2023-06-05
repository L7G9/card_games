"""Contains method for getting the values of a card in a game of 21 Bust.

Methods:

    card_value
    alt_card_value

Typical usage examples:

    card = Card(Value.ACE, Suit.SPADES)

    value = card_value(card)

    alt_value = alt_card_value(card)
"""


from typing import Union

from model.card_game.card import Card


def card_value(card: Card) -> int:
    """The value of a Card when calculating the total of a player's hand.

    Picture cards (values 11, 12 & 13) have a game value of 10.
    All other cards have a game value equal to their enumeration value.

    returns:
        An integer equal to the value of the card in 21 Bust.
    """
    if card.value.value > 10:
        return 10
    else:
        return card.value.value


def alt_card_value(card: Card) -> Union[int, None]:
    """The alternate value of a Card when calculating the total of a
    player's hand.

    Aces can have a game value of 1 or 11.
    All other cards only have one game value.

    returns:
        An integer equal to the alternate game value of the card in
            21 Bust.  Returns None when card is not an Ace and has no
            alternate game value.
    """
    if card.value.value == 1:
        return 11
    else:
        return None
