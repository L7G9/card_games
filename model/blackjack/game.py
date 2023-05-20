import random

from typing import Union

from model.card_game.suit import Suit
from model.card_game.card import Card
from model.card_game.deck import Deck

from model.blackjack.value import Value
from model.blackjack.player import Player
from model.blackjack.player_status import PlayerStatus
from model.blackjack.game_status import GameStatus
from model.blackjack.game_stats import GameStats


class Game:
    """A Game of Blackjack.

    Attributes:
        name: A string describing this game's name.
        deck: A Deck instance representing the cards to be dealt to players in
        this game.
        players: A list of Player instances representing the players in this
        game, what cards are in their hands and their status'.
        status: A GameStatus for the current status of this game.
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
        self.status = GameStatus.DEALING
        self.active_player_index = 0
        self.game_stats: GameStats = None

    def deal(self) -> GameStatus:
        """Deal cards to players.

        Use after Game constructor or reset method is called.

        Gets the game started by shuffling the deck, and dealing 2 cards
        each player.  Initializes active_player_index and active_player_index.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.STARTING_PLAYER to start the 1st player's turn.
        """
        # TODO: check game status
        self.deck.shuffle()
        for i in range(2):
            for player in self.players:
                player.add_card(self.deck.cards.pop())

        self.active_player_index = -1

        self.game_stats = GameStats(len(self.players))

        self.status = GameStatus.STARTING_PLAYER
        return self.status

    def next_player(self) -> GameStatus:
        """Update game ready for the next player.

        Should be called after deal method is called, a player sticks or goes
        bust.

        Use after next_player the resolve_stick_action and the
        resolve_twist_action (resulting in bust) methods are called.

        Moves active_player_index on to the next player.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.GETTING_PLAYER_ACTION when there are more players to go.
              GameStatus.RESOLVING_GAME when all players have been.
        """
        # TODO: check game status
        self.active_player_index += 1

        if self.active_player_index == len(self.players):
            self.status = GameStatus.RESOLVING_GAME
        else:
            self.status = GameStatus.GETTING_PLAYER_ACTION
        return self.status

    def start_turn(self, player: Player) -> GameStatus:
        """Update game ready for the next player.

        Use after next_player and the resolve_twist_action (not
        resulting in bust) methods are called.

        Informs player they need decide whether to stick or twist.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.RESOLVING_PLAYER_ACTION to wait for player to choose
              action.
        """
        # TODO: check game status
        # TODO: rename RESOLVING_PLAYER_ACTION to WAITING_FOR_PLAYER
        if player != self.players[self.active_player_index]:
            return self.status

        player.play()

        self.status = GameStatus.RESOLVING_PLAYER_ACTION
        return self.status

    def resolve_stick_action(
        self,
        player: Player,
    ) -> GameStatus:
        """Resolve a player's stick action.

        Use after start_turn methods is called.

        Sets the player's status.
        Updates game_stats to reflect the change.

        Args:
            player: The Player instance taking the stick action.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.STARTING_PLAYER to start next player's turn.
        """
        # TODO: check game status
        if player != self.players[self.active_player_index]:
            return self.status

        player.stick()
        self.game_stats.update(PlayerStatus.STICK)

        self.status = GameStatus.STARTING_PLAYER
        return self.status

    def resolve_twist_action(
        self,
        player: Player,
    ) -> Union[GameStatus, Card]:
        """Resolve a player's twist action.

        Use after start_turn methods is called.

        Updates the player's status using a card taken from the deck.
        Updates game_stats to reflect the change.

        Args:
            player: The Player instance taking the twist action.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.STARTING_PLAYER to start next player's turn if this
              player went bust.
              GameStatus.GETTING_PLAYER_ACTION for this player to continue if
              this player did not bust.
            The Card instance the player drew.
        """
        # TODO: check game status
        if player != self.players[self.active_player_index]:
            return self.status

        card = self.deck.cards.pop()
        if player.twist(card) == PlayerStatus.BUST:
            self.status = GameStatus.STARTING_PLAYER
            self.game_stats.update(PlayerStatus.BUST)
        else:
            self.status = GameStatus.GETTING_PLAYER_ACTION
        return self.status, card

    def resolve_game(self) -> Union[GameStatus, list[Player]]:
        """Gets finds results of game after all players have been.

        Use after next_player method is called and all players have chosen to
        stick or gone bust.

        Finds the winning players and updates their win_count.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.RESETTING_GAME to get the game ready to play again.
            A list Player instances who won this game.
        """
        # TODO: check game status
        winners = self.get_winners()

        for player in winners:
            player.win_count += 1

        self.status = GameStatus.RESETTING_GAME
        return self.status, winners

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
            if player.status == PlayerStatus.STICK:
                if player.best_total > best_total:
                    # if better then current best_total start new list
                    best_total = player.best_total
                    winners = [player]
                elif player.best_total == best_total:
                    # if same as current best_total add to list
                    winners.append(player)

        return winners

    def reset_game(self, winners: list[Player]) -> GameStatus:
        """Gets finds results of game after all players have been.

        Use after resolve_game method is called.

        Updates the order which the players have their turn next game.
        Returns the cards in each player's hand to the deck.
        Resets each player ready for the next game.

        Args:
            winners: List of Player instances who won this game.

        Returns:
            The GameStatus after this method has been executed.
              GameStatus.DEALING game is ready to deal again.
        """
        # TODO: check game status
        if winners is not None:
            self.players = self.get_player_order(winners)

        for player in self.players:
            self.deck.return_cards(player.hand)
            player.reset()

        self.status = GameStatus.DEALING
        return self.status

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
