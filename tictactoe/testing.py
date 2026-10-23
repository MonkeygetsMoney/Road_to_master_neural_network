import math
EMPTY = None

X = 'X'
O = 'O'
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[O, EMPTY, O],
            [EMPTY, O, EMPTY],
            [O, EMPTY, EMPTY]]

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

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # we can assume that there is only one possible winnin situation (one with 3 in a row)
    for i in range(len(board)):
        check = []
        for j in range(len(board)):
            character = f'{board[i][j]}'
            check.append(character)
        result_check = ''.join(check)

        if result_check == 3*'X' or result_check == 3*'O':
            print(result_check)
            return True
        else:
            check = []

        for j in range(len(board)):
            character = f'{board[j][i]}'
            check.append(character)
        result_check = ''.join(check)
        if result_check == 3*'X' or result_check == 3*'O':
            return True
        else:
            check = []

        for j in range(len(board)):
            character = f'{board[j][j]}'
            check.append(character)
        result_check = ''.join(check)
        if result_check == 3*'X' or result_check == 3*'O':
            return True
        else:
            check = []

        for j in range(len(board)):
            character = f'{board[j][2-j]}'
            check.append(character)
        result_check = ''.join(check)
        if result_check == 3*'X' or result_check == 3*'O':
            return True
        else:
            check = []

    return False
        

board = initial_state()

possible_actions = actions(board)
turn = player(board)
check_game = terminal(board)
print(check_game)
