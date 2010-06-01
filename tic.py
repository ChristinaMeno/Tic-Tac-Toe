#!/usr/bin/env python
import itertools

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

BOARD_SIZE = 3
NUMBER_OF_MOVES = BOARD_SIZE ** 2

def draw_board(board_state):
    '''
        Turn out a crappy ascii representation of the board.
        Numbers representing the position are included so 
        that the user know where his next move will be placed
    '''
    board = range(NUMBER_OF_MOVES)
    for x in range(len(board_state)):
        if x == NUMBER_OF_MOVES:
            break
        if x % 2 == 0:
            board[board_state[x]] = 'X'
        else:   
            board[board_state[x]] = 'O'
        
    rows = tuple(board[x:x+BOARD_SIZE] for x in range(0, NUMBER_OF_MOVES, BOARD_SIZE))
    for r in rows:
        print r

    print '\n'
        

def gen_wins(BOARD_SIZE=3):
    '''
        Each tuple represents a slice of the board where a win can occur.
        They contain the offsets that represent rows columns and diagonals
        i.e. diags contain (0,4,6) and (2,4,8)
    '''
    board = tuple(xrange(NUMBER_OF_MOVES))
    rows = tuple(board[x:x+BOARD_SIZE] for x in range(0, NUMBER_OF_MOVES, BOARD_SIZE))

    board = tuple(board[x] for y in range(BOARD_SIZE) for x in range(y, NUMBER_OF_MOVES, BOARD_SIZE))
    cols = tuple(board[x:x+BOARD_SIZE] for x in range(0, NUMBER_OF_MOVES, BOARD_SIZE))

    diags = (tuple(x for x in range(0, NUMBER_OF_MOVES, BOARD_SIZE + 1)),
            tuple(x for x in range(BOARD_SIZE - 1, NUMBER_OF_MOVES - 1, BOARD_SIZE - 1)))

    return rows +\
           cols +\
           diags

  
def has_won(current_state):
    '''
        returns: True if there is a winning state on the board for either player, False otherwise
        this is determined by comparing the odds and evens of the current_state. Those represent the moves
        made by a single player. Comparing the combinations of size three with the winning offsets will identify a win
    '''
    #GM good candidate for class member
    wins = gen_wins()
     
    winning_state = False
    evens = tuple(current_state[i] for i in range(0, len(current_state), 2))
    odds  = tuple(current_state[i] for i in range(1, len(current_state), 2))

    #print evens, odds
    for y in wins:
        for z in itertools.combinations(evens, BOARD_SIZE):
            if set(y) - set(z)  == set(()):
                #print 'EVEN', y , z
                winning_state = True
        for a in itertools.combinations(odds, BOARD_SIZE):
            if set(y) - set(a)  == set(()):
                #print 'ODD', y, a
                winning_state = True

    #print winning_state
    return winning_state

    
def choose_move(current_state, iter_count=0):

    #you can't win in the next transition if you only got one other token on the board
    #so introduce some special cases for opening moves
    if len(current_state) in (0, 1):
        if 0 not in current_state:
            return 0
        elif 4 not in current_state:
            return 4

    remaining_moves = tuple(x for x in range(NUMBER_OF_MOVES) if x not in current_state) 

    print remaining_moves, current_state

    if not len(remaining_moves) or iter_count > len(remaining_moves):
        return remaining_moves[0]
        #return None 

    #choose a wining move for computer
    for x in remaining_moves:
        next_state = current_state + (x,)
        if has_won(next_state):
            #print '%s, IS A win in state %s' %(str(x), str(iter_count))
            return x 

    #choose no state, and see if the next move could be a win
    return choose_move(current_state + (-1,), iter_count + 1)
        
    

def run_game(current_state):
    '''
        Displays available move to choose
        Interactively asks human player for a move
        draws boards and determines winner
    ''' 
    draw_board(current_state)
    
    #human plays the even moves
    human_plays = 0
    current_player = 'human'

    while len(current_state ) < NUMBER_OF_MOVES:
        remaining_moves = tuple(x for x in range(NUMBER_OF_MOVES) if x not in current_state) 

        if len(current_state) % 2 == human_plays:
            #player chooses
            current_player = 'human'
            next_move = -1
            while next_move not in remaining_moves:
                next_move = int(raw_input(str(remaining_moves)))
                #print type(human_choice)

        else:
            #comupter chooses
            current_player = 'computer'
            next_move = choose_move(current_state)
            print 'Computer choose:',  next_move

        #update state and draw_board
        current_state = current_state + (next_move,) 
        print '%d moves have been made'% len(current_state)
        draw_board(current_state)

        #check for a win
        if has_won(current_state):
            print '%s won' % current_player
            break

    if not has_won(current_state):
        print 'tie game'

if __name__ == '__main__':
    ''' 
    #TEST ODDS and EVENS in has_won()
    for x in range(NUMBER_OF_MOVES):
        current_state = tuple(xrange(x))
        has_won(current_state)
    '''
    current_state = ()
    run_game(current_state)
