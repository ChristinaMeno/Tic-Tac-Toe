import itertools
import sys

'''
GM: this is how the tuple that represents board state is organized
    current_state = (0, 8, 4,) represents a game in which three moves have been made
    currently odd moves are marked by an X and even moves are O. Each element of the tuple
    is an index on the board layout below.

for a size three board:
    0 1 2
    3 4 5
    6 7 8

for a size four board
    0  1  2  3
    4  5  6  7
    8  9  10 11
    12 13 14 15
'''

def draw_board(board_state, board_size=3):
    board = range(9)
    for x in range(len(board_state)):
        if x % 2 == 0:
            board[board_state[x]] = 'X'
        else:   
            board[board_state[x]] = 'O'
        
    rows = tuple(board[x:x+board_size] for x in range(0, board_size ** 2, board_size))
    for r in rows:
        print r

    print '\n'
        

def gen_wins(board_size=3):
    board = tuple(xrange(board_size ** 2))
    rows = tuple(board[x:x+board_size] for x in range(0, board_size ** 2, board_size))

    board = tuple(board[x] for y in range(board_size) for x in range(y, board_size ** 2, board_size))
    cols = tuple(board[x:x+board_size] for x in range(0, board_size ** 2, board_size))

    diags = (tuple(x for x in range(0, board_size ** 2, board_size + 1)),
            tuple(x for x in range(board_size - 1, board_size ** 2 - 1, board_size - 1)))

    return rows +\
           cols +\
           diags

  
def has_won(current_state, board_size=3):
    #GM good candidate for class member
    wins = gen_wins()
     
    winning_state = False
    evens = tuple(current_state[i] for i in range(0, len(current_state), 2))
    odds  = tuple(current_state[i] for i in range(1, len(current_state), 2))

    print evens, odds
    for y in wins:
        for z in itertools.combinations(evens, board_size):
            if set(y) - set(z)  == set(()):
                print 'EVEN', y , z
                winning_state = True
        for a in itertools.combinations(odds, board_size):
            if set(y) - set(a)  == set(()):
                print 'odd', y, a
                winning_state = True

    print winning_state
    return winning_state

    
if __name__ == '__main__':
    #TEST ODDS and EVENS in has_won()
    for x in range(9):
        current_state = tuple(xrange(x))
        has_won(current_state)
