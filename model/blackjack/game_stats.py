from model.blackjack.player_status import PlayerStatus


class GameStats:
    """Stats for all the other player states in the game."""
    def __init__(self, player_count: int):
        self.player_count = player_count
        self.waiting_count = self.player_count
        self.sticking_count = 0
        self.bust_count = 0

    def update(self, player_status: PlayerStatus):
        self.waiting_count -= 1
        if player_status is PlayerStatus.STICK:
            self.sticking_count += 1
        if player_status is PlayerStatus.BUST:
            self.bust_count += 1

    def reset(self):
        self.waiting_count = self.player_count
        self.sticking_count = 0
        self.bust_count = 0
