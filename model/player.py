from card_group import CardGroup


class Player:
    """Class to represent a player in a card game.

    Attributes:
        name: A string describing this player.
        hand: A CardGroup for the Cards this player is holding.
    """
    def __init__(self, name: str, hand: CardGroup):
        self.name = name
        self.hand = hand
