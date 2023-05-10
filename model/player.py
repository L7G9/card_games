from model.card_group import CardGroup


class Player:
    """Class to represent a player in a card game.

    Attributes:
        id: An int to uniquely identify a player.
        name: A string describing this player.
        hand: A CardGroup for the Cards this player is holding.
    """
    def __init__(self, id: int, name: str, hand: CardGroup):
        self.id = id
        self.name = name
        self.hand = hand
