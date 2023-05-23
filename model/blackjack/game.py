import random
from typing import Union

from model.blackjack.game_state import GameState
from model.blackjack.game_state_error import GameStateError
from model.blackjack.game_stats import GameStats
from model.blackjack.player import Player
from model.blackjack.player_order_error import PlayerOrderError
from model.blackjack.player_state import PlayerState
from model.blackjack.value import Value
from model.card_game.card import Card
from model.card_game.deck import Deck
from model.card_game.suit import Suit


class Game:
    """A Game of Blackjack.

    Contains a set of methods to be called in order to progress through a
    simplified game of Blackjack with the following rules...
    - There is a single deck of 52 standard playing cards.
    - Aces can be worth 1 or 11, picture cards (Jacks, Queens & Kings) are
      worth 10, all other cards are worth their face value.
    - Each player is dealt 2 cards face down.
    - The dealer does not play a hand.
    - Each player has a turn in which they can draw a card by choosing to
      twist or end their turn by choosing to stick.  After choosing to
      twist, if they don't have a total value in their hand equal to under
      21 they go bust.
    - After all players have had a turn they reveal their cards.  The players
      with the highest total under or equal to 21 win.
    - The next time the game is played

    Attributes:
        name: A string describing this game's name.
        deck: A Deck instance representing the cards to be dealt to players in
        this game.
        players: A list of Player instances representing the players in this
        game, what cards are in their hands and their state'.
        state: A GameState for the current state of this game.
        active_player_index: An integer holding the index of the Player
        instance in players who's turn it currently is.
        game_stats: A GameStats instance hold details of how many players
        have yet to complete their turn, have gone bust and so on.
    """

    def __init__(self, name: str):
        """Initializes instance.

        Args:
            name: A string describing this game's name.
        """
        self.name = name
        self.deck = Deck("Deck", Value, Suit)
        self.players: list[Player] = []
        self.state = GameState.DEALING
        self.active_player_index = -1
        self.game_stats: GameStats = None

    def deal(self) -> GameState:
        """Deal cards to players.

        Use after Game constructor or reset method is called.

        Gets the game started by shuffling the deck, and dealing 2 cards
        each player.  Initializes active_player_index and active_player_index.

        Returns:
            The GameState after this method has been executed.
              GameState.GETTING_NEXT_PLAYER to start the 1st player's turn.

        Raises:
            GameStateError: If state is not DEALING.
        """
        if self.state is not GameState.DEALING:
            raise GameStateError(self.state, [GameState.DEALING])

        self.deck.shuffle()
        for i in range(2):
            for player in self.players:
                player.add_card(self.deck.cards.pop())

        self.active_player_index = -1

        self.game_stats = GameStats(len(self.players))

        self.state = GameState.GETTING_NEXT_PLAYER
        return self.state

    def next_player(self) -> GameState:
        """Update game ready for the next player.

        Should be called after deal method is called, a player sticks or goes
        bust.

        Use after next_player the resolve_stick_action and the
        resolve_twist_action (resulting in bust) methods are called.

        Moves active_player_index on to the next player.

        Returns:
            The GameState after this method has been executed.
              GameState.STARTING_PLAYER_TURN when players are waiting to
              play.
              GameState.RESOLVING_GAME when all players have been.

        Raises:
            GameStateError: If state is not GETTING_NEXT_PLAYER.
        """
        if self.state is not GameState.GETTING_NEXT_PLAYER:
            raise GameStateError(self.state, [GameState.GETTING_NEXT_PLAYER])

        self.active_player_index += 1

        if self.active_player_index == len(self.players):
            self.state = GameState.RESOLVING_GAME
        else:
            self.state = GameState.STARTING_PLAYER_TURN
        return self.state

    def start_turn(self, player: Player) -> GameState:
        """Update game ready for the next player.

        Use after next_player and the resolve_twist_action (not
        resulting in bust) methods are called.

        Informs player they need decide whether to stick or twist.

        Returns:
            The GameState after this method has been executed.
              GameState.WAITING_FOR_PLAYER to wait for player to choose
              action.

        Raises:
            GameStateError: If state is not STARTING_PLAYER_TURN.
        """

        if self.state is not GameState.STARTING_PLAYER_TURN:
            raise GameStateError(self.state, [GameState.STARTING_PLAYER_TURN])

        if player != self.players[self.active_player_index]:
            return self.state

        player.play()

        self.state = GameState.WAITING_FOR_PLAYER
        return self.state

    def resolve_stick_action(
        self,
        player: Player,
    ) -> GameState:
        """Resolve a player's stick action.

        Use after start_turn methods is called.

        Sets the player's state.
        Updates game_stats to reflect the change.

        Args:
            player: The Player instance taking the stick action.

        Returns:
            The GameState after this method has been executed.
              GameState.GETTING_NEXT_PLAYER to start next player's turn.

        Raises:
            GameStateError: If state is not WAITING_FOR_PLAYER.
            PlayerOrderError: If player is not players[active_player_index].
        """
        if self.state is not GameState.WAITING_FOR_PLAYER:
            raise GameStateError(self.state, [GameState.WAITING_FOR_PLAYER])

        active_player = self.players[self.active_player_index]
        if player is not active_player:
            raise PlayerOrderError(player, active_player)

        player.stick()
        self.game_stats.update(PlayerState.STICK)

        self.state = GameState.GETTING_NEXT_PLAYER
        return self.state

    def resolve_twist_action(
        self,
        player: Player,
    ) -> Union[GameState, Card]:
        """Resolve a player's twist action.

        Use after start_turn methods is called.

        Updates the player's state using a card taken from the deck.
        Updates game_stats to reflect the change.

        Args:
            player: The Player instance taking the twist action.

        Returns:
            The GameState after this method has been executed.
              GameState.GETTING_NEXT_PLAYER to start next player's turn if this
              player went bust.
              GameState.STARTING_PLAYER_TURN for this player to continue if
              this player did not bust.
            The Card instance the player drew.

        Raises:
            GameStateError: If state is not WAITING_FOR_PLAYER.
            PlayerOrderError: If player is not players[active_player_index].
        """
        if self.state is not GameState.WAITING_FOR_PLAYER:
            raise GameStateError(self.state, [GameState.WAITING_FOR_PLAYER])

        active_player = self.players[self.active_player_index]
        if player is not active_player:
            raise PlayerOrderError(player, active_player)

        card = self.deck.cards.pop()
        if player.twist(card) == PlayerState.BUST:
            self.state = GameState.GETTING_NEXT_PLAYER
            self.game_stats.update(PlayerState.BUST)
        else:
            self.state = GameState.STARTING_PLAYER_TURN
        return self.state, card

    def resolve_game(self) -> Union[GameState, list[Player]]:
        """Gets finds results of game after all players have been.

        Use after next_player method is called and all players have chosen to
        stick or gone bust.

        Finds the winning players and updates their win_count.

        Returns:
            The GameState after this method has been executed.
              GameState.RESETTING_GAME to get the game ready to play again.
            A list Player instances who won this game.

        Raises:
            GameStateError: If state is not RESOLVING_GAME.
        """
        if self.state is not GameState.RESOLVING_GAME:
            raise GameStateError(self.state, [GameState.RESOLVING_GAME])

        winners = self.get_winners()

        for player in winners:
            player.win_count += 1

        self.state = GameState.RESETTING_GAME
        return self.state, winners

    def get_winners(self) -> list[Player]:
        """Finds winners of this game of Blackjack.

        Use after next_player method is called and all players have been.

        Search for winners by looking for the players who have stuck and have
        highest best_total.

        Returns:
            A list Player instances who won this game.
        """
        winners = []
        best_total = 0

        for player in self.players:
            player.reveal_hand()
            if player.state == PlayerState.STICK:
                if player.best_total > best_total:
                    # if better then current best_total start new list
                    best_total = player.best_total
                    winners = [player]
                elif player.best_total == best_total:
                    # if same as current best_total add to list
                    winners.append(player)

        return winners

    def reset_game(self, winners: list[Player]) -> GameState:
        """Gets finds results of game after all players have been.

        Use after resolve_game method is called.

        Updates the order which the players have their turn next game.
        Returns the cards in each player's hand to the deck.
        Resets each player ready for the next game.

        Args:
            winners: List of Player instances who won this game.

        Returns:
            The GameState after this method has been executed.
              GameState.DEALING game is ready to deal again.

        Raises:
            GameStateError: If state is not RESETTING_GAME.
        """
        if self.state is not GameState.RESETTING_GAME:
            raise GameStateError(self.state, [GameState.RESETTING_GAME])

        if winners is not None:
            self.players = self.get_player_order(winners)

        for player in self.players:
            self.deck.return_cards(player.hand)
            player.reset()

        self.state = GameState.DEALING
        return self.state

    def get_player_order(self, winners: list[Player]) -> list[Player]:
        """Get an updated player order based on the which player won this
        game.

        Chooses one winner at random.  That winner is placed at the start of
        the list and has to go first next round. The remaining players are
        added, starting with any after the winner, then any before.  This
        gives the effect of players sitting round a table, the player who
        starts changes but the direction of the next player always the same.

        Args:
            winners: List of Player instances who won this game.

        Returns:
            List of Player instances in the new playing order.
        """
        # check for no winners
        if not winners:
            return None

        # get index of one random winner
        winner = random.choice(winners)
        winner_index = self.players.index(winner)

        # create new list with chosen winner a the front
        players = []
        for index in range(winner_index, len(self.players)):
            players.append(self.players[index])
        for index in range(0, winner_index):
            players.append(self.players[index])

        return players
