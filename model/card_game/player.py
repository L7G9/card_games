from model.card_game.card_group import CardGroup


class Player:
    """Class to represent a player in a card game.

    Attributes:
        id: An int to uniquely identify a player.
        name: A string describing this player.
        hand: A CardGroup for the Cards this player is holding.
    """
    def __init__(self, id: int, name: str):
        """Initializes instance.

        Args:
            id: An unique integer id.
            name: A string for the player's name.
        """
        # TODO: remove id
        self.id = id
        self.name = name
        self.hand = CardGroup("%s's hand" % (name))
