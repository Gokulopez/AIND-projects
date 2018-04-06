"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
     # Return '-inf' if the game is a lose, 'inf' if a win
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Assign a weight to use for the opponent's moves
    weight = 1.6

    # Get each player's number of legal moves
    own_moves = len(game.get_legal_moves(player))
    # Include the weight to the opponent's legal moves
    opp_moves = weight * len(game.get_legal_moves(game.get_opponent(player)))

    # Return the calculated heuristic value
    return float(own_moves - opp_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves_y, own_moves_x = game.get_player_location(player)
    opp_moves_y, opp_moves_x = game.get_player_location(game.get_opponent(player))

    diff_in_y = own_moves_y - opp_moves_y 
    diff_in_x = own_moves_x - opp_moves_x 
    # Closer the opponents the better
    return -float( diff_in_y**2 + diff_in_x**2)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # Return '-inf' if the game is a lose, 'inf' if a win
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Calculate and return the sum of the number of the player's moves and the remaining open spaces
    return float(len(game.get_legal_moves(player)) + len(game.get_blank_spaces()))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        def max_value(game, depth):
            """This is a helper method for minimax to evaluate the max value from the node's children
            Parameters
            ----------
            state : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state
            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting
            Returns
            -------
            float
                max value that was evaluated from the current node's children or utility value
                from the current player's perspective if a terminal state or max depth is reached
            """

            # Evaluate and return the score of the current state if the current state has no
            # more legal moves or if the maximum allowed depth had been reached
            if not game.get_legal_moves() or depth <= 0:
                return self.score(game, self)

            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # Initialize the maxi_value so that this method returns something in case time runs out
            maxi_value = float('-inf')
            # Iterate through all the player's moves to find the max value from the current node's children
            for move in game.get_legal_moves():
                maxi_value = max(maxi_value, min_value(game.forecast_move(move), depth - 1))

            return maxi_value
        
        def min_value(game, depth):
            """This is a helper method for minimax to evaluate the minimum value from the node's children
            Parameters
            ----------
            state : isolation.Board
                An instance of the Isolation game `Board` class representing the
                current game state
            depth : int
                Depth is an integer representing the maximum number of plies to
                search in the game tree before aborting
            Returns
            -------
            float
                minimum value that was evaluated from the current node's children or utility value
                from the current player's perspective if a terminal state or max depth is reached
            """

            # Evaluate and return the score of the current state if the current state has no
            # more legal moves or if the maximum allowed depth had been reached
            if not game.get_legal_moves() or depth <= 0:
                return self.score(game, self)
    
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            # Initialize the mini_value so that this method returns something in case time runs out
            mini_value = float('inf')
            # Iterate through all the player's moves to find the min value from the current node's children
            for move in game.get_legal_moves():
                mini_value = min(mini_value, max_value(game.forecast_move(move), depth - 1))
            return mini_value
        

        best_move = (-1, -1)
        best_value = float('-inf')
        legal_moves = game.get_legal_moves()
        
        # Return best_move's current state if the agent is out of legal moves else
        # assign the best move a random value in case time runs out
        if not legal_moves:
            return best_move
        else:
            best_move = legal_moves[random.randint(0, len(legal_moves)) - 1]

        
        # Iterate through the moves to calculate each move's minimax value
        for move in legal_moves:
            value = min_value(game.forecast_move(move), depth - 1)

            # Update best_value and best_move when a better value is found
            if value >= best_value:
                best_value = value
                best_move = move

        return best_move

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        # TODO: finish this function!

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            # I use while true instead of using a for loop to infinity
            depth = 1
            while True: 
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha = float('-inf'), beta = float('inf')):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        def max_value(game, alpha, beta, depth):
            
            #check if we are out of moves or reached the depth limit
            if not game.get_legal_moves() or depth <= 0:
                return self.score(game, self)

            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            
            # Initialize the max_value so that this method returns something in case time runs out
            max_value = float('-inf')
            # Iterate through all the player's moves to find the max value from the current node's children
            for move in game.get_legal_moves():
                max_value = max(max_value, min_value(game.forecast_move(move), alpha, beta, depth - 1))
               
                # Return the max value when it becomes larger than beta
                if max_value >= beta:
                    return max_value
                # Update alpha if the max value is greater than alpha
                alpha = max(alpha, max_value)

            return max_value

        def min_value(game, alpha, beta, depth):

            #check if we are out of moves or reached the depth limit
            if not game.get_legal_moves() or depth <= 0:
                return self.score(game, self)
    
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # Initialize the max_value so that this method returns something in case time runs out
            min_value = float('inf')

            # Iterate through all the player's moves to find the max value from the current node's children
            for move in game.get_legal_moves():
                min_value = min(min_value, max_value(game.forecast_move(move), alpha, beta, depth - 1))
                if min_value <= alpha:
                    return min_value
                # Update alpha if the max value is greater than alpha
                beta = min(beta, min_value)
            return min_value
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)
        best_value = float('-inf')
        legal_moves = game.get_legal_moves()

        # Return best_move's current state if the agent is out of legal moves else
        # assign the best move a random value in case time runs out
        if not legal_moves:
            return best_move
        else:
            best_move = legal_moves[random.randint(0, len(legal_moves)) - 1]
        
        # Iterate through the moves to calculate each move's minimax value
        for move in legal_moves:
            value = min_value(game.forecast_move(move), alpha, beta, depth - 1)
            
            # Update best_value and best_move when a better value is found
            if value > best_value:
                best_value = value
                best_move = move
            # Return the best value when it becomes larger than beta
            if best_value >= beta:
                return best_move
            # Update alpha if the best value is greater than alpha
            alpha = max(alpha, best_value)

        return best_move