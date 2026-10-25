"""
Tic Tac Toe Player
"""

import math
import copy
import random

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = {
        'X': 0,
        'O': 0
    }
    # check the count of X and O

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                count[X] += 1
            elif board[i][j] == O:
                count[O] += 1

    total = 0 # how many characters currently on the board
    for character in count:
        total += count[character]

    if total % 2 == 0:
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                possible_actions.add((i, j))
            else: continue

    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # action is only one move at a time
    # make deep copy at the result function
    # check the current action
    i, j = action
    result_board = copy.deepcopy(board)
    turn = player(result_board) # either X or O
    try:
        result_board[i][j] = turn
        if board[i][j] == EMPTY:
            return result_board
        elif board[i][j] is X or board[i][j] is O:
            raise ValueError('Move already occupies')
    except IndexError:
        raise ValueError('Move out of bound')
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning = ['XXX', 'OOO']
    for i in range(len(board)):
        # put dict here to reset for each iteration
        check = {
            'row': [],
            'column': [],
            'l_diagonal': [],
            'r_diagonal': []
        }
        for j in range(len(board[i])):
            check['row'].append(f'{board[i][j]}')
            check['column'].append(f'{board[j][i]}')
            check['l_diagonal'].append(f'{board[j][j]}')
            check['r_diagonal'].append(f'{board[j][2-j]}')

        for check_game in check:
            row = ''.join(check[check_game])
            if row == winning[0]:
                return X
            elif row == winning[1]:
                return O
            else:
                continue

    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if bool(winner(board)):
        return True
    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] is EMPTY:
                    return False
                else:
                    continue

        return True
    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        # if nothing just return 0
        return 0

    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    moves = {}
    if terminal(board):
        return None
    else:
        if player(board) == X:
            for action in actions(board):
                maximize = max_value(result(board, action))
                minimize = min_value(result(board, action))
                moves[action] = minimize
            # get the max values in the dict
            max_move = max(moves, key=moves.get)
            print(moves)
            return max_move                
        elif player(board) == O:
            for action in actions(board):
                maximize = max_value(result(board, action))
                minimize = min_value(result(board, action))
                moves[action] = maximize # list all maximize scores from the move
            min_move = min(moves, key=moves.get) # since it's minimize, will choose the lowest score
            print(moves)
            return min_move
    raise NotImplementedError

board = initial_state()
print(result(board, (-3, 5)))
