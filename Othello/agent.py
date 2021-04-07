"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

# Keys: board state tuples (board, color)
# Values: the best move and minimax value of the board state tuples (best_move, minmax)
cache = dict()


def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    # get_score(board) returns a tuple (number of dark disks, number of light disks)
    result = get_score(board)

    # utility calculated as the number of disks of the player's colour minus the number of disks of the opponent
    if color == 1:
        return result[0] - result[1]
    else:
        return result[1] - result[0]


# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    # IMPLEMENT
    # Board size
    d = len(board)

    # Minimize the number of disks the opponent
    result = get_score(board)
    if color == 1:
        utility = result[0] - result[1]
    else:
        utility = result[1] - result[0]

    # Minimize the number of moves the opponent can make
    dark_moves = len(get_possible_moves(board, 1))
    light_moves = len(get_possible_moves(board, 2))
    if color == 1:
        mobility = dark_moves - light_moves
    else:
        mobility = light_moves - dark_moves

    # Check board size to prevent index out of range
    if d < 4:
        return utility + mobility

    # Now the rest satisfies board size >= 4
    dark = 0
    light = 0

    # Highly value taking corner fields
    corners = [(0, 0), (d - 1, 0), (0, d - 1), (d - 1, d - 1)]
    for (column, row) in corners:
        if board[column][row] == 1:
            dark += 500
        elif board[column][row] == 2:
            light += 500

    # Highly penalize taking the fields next to the corners
    near_corners = [(1, 0), (0, 1), (1, d - 1), (d - 1, 1), (0, d - 2), (d - 2, 0), (d - 1, d - 2), (d - 2, d - 1)]
    for (column, row) in near_corners:
        if board[column][row] == 1:
            dark -= 50
        elif board[column][row] == 2:
            light -= 50

    # Value other border tiles than remaining tiles
    for i in range(2, d - 2):
        edges = [(0, i), (i, 0), (i, d - 1), (d - 1, i)]
        for (column, row) in edges:
            if board[column][row] == 1:
                dark += 50
            elif board[column][row] == 2:
                light += 50

    if color == 1:
        weight = dark - light
    else:
        weight = light - dark

    return utility + mobility + weight


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    # IMPLEMENT (and replace the line below)
    # Get the opponent
    opponent = 3 - color

    # Check cache
    if caching and (board, color) in cache:
        return cache[(board, color)]

    best_move = None
    min_utility = float('inf')
    possible_moves = get_possible_moves(board, opponent)

    # Check if limit reached or end of game
    if limit == 0 or len(possible_moves) == 0:
        return None, compute_utility(board, color)

    for move in possible_moves:
        # Get the next board
        nxt_board = play_move(board, opponent, move[0], move[1])

        # Compute next utility
        _, nxt_utility = minimax_max_node(nxt_board, color, limit - 1, caching)

        if min_utility > nxt_utility:
            best_move = move
            min_utility = nxt_utility

    # Cache the board
    if caching:
        cache[(board, color)] = (best_move, min_utility)

    return best_move, min_utility


def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT (and replace the line below)
    # Check cache
    if caching and (board, color) in cache:
        return cache[(board, color)]

    best_move = None
    max_utility = float('-inf')
    possible_moves = get_possible_moves(board, color)

    # Check if limit reached or end of game
    if limit == 0 or len(possible_moves) == 0:
        return None, compute_utility(board, color)

    for move in possible_moves:
        # Get the next board
        nxt_board = play_move(board, color, move[0], move[1])

        # Compute next utility
        _, nxt_utility = minimax_min_node(nxt_board, color, limit - 1, caching)

        if max_utility < nxt_utility:
            best_move = move
            max_utility = nxt_utility

    # Cache the board
    if caching:
        cache[(board, color)] = (best_move, max_utility)

    return best_move, max_utility


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enforce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a
    heuristic value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    #IMPLEMENT (and replace the line below)
    return minimax_max_node(board, color, limit, caching)[0]


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    # Get the opponent
    opponent = 3 - color

    # Check cache
    if caching and (board, color) in cache:
        return cache[(board, color)]

    best_move = None
    min_utility = float('inf')
    possible_moves = get_possible_moves(board, opponent)

    # Check if limit reached or end of game
    if limit == 0 or len(possible_moves) == 0:
        return None, compute_utility(board, color)

    # Order (move, board) tuples according to the utility successor states
    move_and_board = []
    for move in possible_moves:
        nxt_board = play_move(board, opponent, move[0], move[1])
        move_and_board.append((move, nxt_board))
    if ordering:
        move_and_board.sort(key=lambda move_and_board: compute_utility(move_and_board[1], color), reverse=False)

    for (move, nxt_board) in move_and_board:
        # Compute next utility
        _, nxt_utility = alphabeta_max_node(nxt_board, color, alpha, beta, limit - 1, caching, ordering)
        if min_utility > nxt_utility:
            best_move = move
            min_utility = nxt_utility
        # Prune
        beta = min(beta, min_utility)
        if alpha >= beta:
            break

    # Cache the board
    if caching:
        cache[(board, color)] = (best_move, min_utility)

    return best_move, min_utility


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    # Check cache
    if caching and (board, color) in cache:
        return cache[(board, color)]

    best_move = None
    max_utility = float('-inf')
    possible_moves = get_possible_moves(board, color)

    # Check if limit reached or end of game
    if limit == 0 or len(possible_moves) == 0:
        return None, compute_utility(board, color)

    # Order (move, board) tuples according to the utility successor states
    move_and_board = []
    for move in possible_moves:
        nxt_board = play_move(board, color, move[0], move[1])
        move_and_board.append((move, nxt_board))
    if ordering:
        move_and_board.sort(key=lambda move_and_board: compute_utility(move_and_board[1], color), reverse=True)

    for (move, nxt_board) in move_and_board:
        # Compute next utility
        _, nxt_utility = alphabeta_min_node(nxt_board, color, alpha, beta, limit - 1, caching, ordering)
        if max_utility < nxt_utility:
            best_move = move
            max_utility = nxt_utility
        # Prune
        alpha = max(alpha, max_utility)
        if alpha >= beta:
            break

    # Cache the board
    if caching:
        cache[(board, color)] = (best_move, max_utility)

    return best_move, max_utility


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    return alphabeta_max_node(board, color, float('-inf'), float('inf'), limit, caching, ordering)[0]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
