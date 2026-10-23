import math
EMPTY = None

X = 'X'
O = 'O'
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

board = initial_state()
possible_actions = actions(board)
turn = player(board)
print(possible_actions, f'current turn is {turn}')
