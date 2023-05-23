from model.blackjack.game_state import GameState


class GameStateError(Exception):
    """Game State Error.

    Occur when the order which a method in Game is called is incompatible with
    it's state.
    For example when deal is called and the game state is WAITING_FOR_PLAYER.
    """

    def __init__(
        self, current_state: GameState, expected_states: list[GameState]
    ):
        self.current_state = current_state
        self.expected_state = expected_states

    def __str__(self):
        return "Current State=%s Expected States=%s" % (
            self.current_state,
            self.expected_state,
        )
