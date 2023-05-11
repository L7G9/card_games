from enum import Enum


class BlackJackValue(Enum):
    def __str__(self) -> str:
        return self.name

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

    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
