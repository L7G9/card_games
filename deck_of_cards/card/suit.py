from enum import Enum

class Suit(Enum):
    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    Clubs = 1
    Diamonds = 2
    Hearts = 3
    Spades = 4
