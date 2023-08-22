"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def count_xo(board):
    """
    Returns number of Xs and Os.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            if cell == O:
                o_count += 1
    return x_count, o_count

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If empty board, then it's X's turn by default because X is always first
    if board == initial_state():
        return X
    else:
        x_count, o_count = count_xo(board)
        # If there are more Xs than Os currently, then next player is O
        if x_count > o_count:
            return O
        # If there equal numbers of Xs and Os currently, then next player is X
        elif x_count == o_count:
            return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3): # Loop thru rows
        for j in range(3): # Loop thru row
            if board[i][j] is EMPTY:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Raise exception if the action is invalid
    if board[action[0]][action[1]]:
        raise ValueError
    if action[0] > 2 or action[0] < 0 or action[1] > 2 or action[1] < 0:
        raise IndexError

    # Make a copy of the board and apply next player to it
    next_player = player(board)
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = next_player
    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check first row
    if board[0][0] and board[0][0] == board[0][1] and board[0][1] == board[0][2]:
        return board[0][0]
    # Check second row
    if board[1][0] and board[1][0] == board[1][1] and board[1][1] == board[1][2]:
        return board[1][0]
    # Check third row
    if board[2][0] and board[2][0] == board[2][1] and board[2][1] == board[2][2]:
        return board[2][0]
    # Check first column
    if board[0][0] and board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    # Check second column
    if board[0][1] and board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    # Check third column
    if board[0][2] and board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]
    # Check forward diagonal
    if board[0][0] and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    # Check backward diagonal
    if board[0][2] and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    x_count, o_count = count_xo(board)
    if winner(board) or (x_count + o_count == 9):
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0

def maximizer(board):
    v = float('-inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, minimizer(result(board, action)))
    return v

def minimizer(board):
    v = float('inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maximizer(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        v = float('-inf')
        moves = []
        for action in actions(board):
             # Store each minimized subtree value alonside the action
             moves.append((minimizer(result(board, action)), action))
        # Sort descendingly to get the max of all minimized results
        return sorted(moves, reverse=True)[0][1]
    
    elif player(board) == O:
        v = float('inf')
        moves = []
        for action in actions(board):
             # Store each maximized subtree root alonside the action
             moves.append((maximizer(result(board, action)), action))
        # Sort ascendingly to get the min of all maximized results
        return sorted(moves)[0][1]