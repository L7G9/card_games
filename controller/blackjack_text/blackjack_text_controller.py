from model.blackjack import blackjack_game as game
from view.text_view import text_view as view


class BlackjackTextController:
    """Controller for BlackJackGame and TextView."""
    def __init__(self):
        self.game = game.BlackjackGame("Blackjack")
        self.view = view.TextView()

    # get player name
    # get number of players
    # set up game
    # run game
    # get restart
    # restart game
