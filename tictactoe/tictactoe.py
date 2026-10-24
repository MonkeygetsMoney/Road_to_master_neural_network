"""
Tic Tac Toe Player
"""

import math

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
        for j in range(len(board[j])):
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
    possible_actions = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                possible_actions.append((i, j))
            else: continue

    return possible_actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
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
            if row in winning:
                return True
            else:
                continue

    return False
    
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
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
            if row is winning[0]:
                return 1
            elif row is winning[1]:
                return -1

    # if nothing just return 0
    return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    raise NotImplementedError

board = initial_state()
check_result = terminal(board)
print(check_result)