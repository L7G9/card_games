from enum import Enum


class BlackJackValue(Enum):
    def __str__(self) -> str:
        return self.name.capitalize()

    def __int__(self) -> int:
        return self.game_value()

    def game_value(self) -> int:
        """Make all picture cards worth 10."""
        if self.value > 10:
            return 10
        else:
            return self.value

    def alt_game_value(self) -> int:
        """Aces have an alternate in game value of 11."""
        if self.value == 1:
            return 11
        else:
            return self.value

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
