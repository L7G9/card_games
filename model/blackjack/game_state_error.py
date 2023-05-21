class GameStateError(Exception):
    """Game State Error

    Occur when the order which a method in Game is called is incompatible with
    it's state.
    For example when deal is called and the game state is WAITING_FOR_PLAYER.
    """
    def __init__(self):
        pass

    def __str__(self):
        return ("Game State error occurred")
