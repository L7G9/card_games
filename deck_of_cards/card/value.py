from enum import Enum

class Value(Enum):
    def __str__(self):
        return self.name

    def __int__(self):
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
