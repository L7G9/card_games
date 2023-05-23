from enum import Enum


class Value(Enum):
    """Values of the playing cards in a game of BlackJack.

    Attributes:
        name: A string for the name of the card from Ace to King.
        value: An integer unique to each member in this enumeration.
    """

    def __str__(self) -> str:
        """Return name as a display friendly string."""
        return self.name.capitalize()

    def game_value(self) -> int:
        """The value of Card when calculating the total of a player's hand.

        Picture cards (values 11, 12 & 13) have a game value of 10.
        All other cards have a game value equal to their enumeration value.

        returns:
            An integer equal to the value of the card in Blackjack.
        """
        if self.value > 10:
            return 10
        else:
            return self.value

    def alt_game_value(self) -> int:
        """The alternate game value of Card when calculating the total of a
        player's hand.

        Aces can have a game value of 1 or 11.
        All other cards only have one game value.

        returns:
            An integer equal to the alternate game value of the card in
            Blackjack.  Returns None when card is not an Ace and has no
            alternate game value.
        """
        if self.value == 1:
            return 11
        else:
            return None

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
