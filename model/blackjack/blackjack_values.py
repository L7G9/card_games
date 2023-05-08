from value import Value


class BlackJackValues(Value):
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
