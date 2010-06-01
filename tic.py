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

def get_set_not_blocked(players_moves, remaining_moves):
    wins = gen_wins()
    for i in wins:
        if set(i) - set(players_moves) == set(i):
            u  = tuple((j for j in i if j in remaining_moves))
            if len(u):
                return u[0]

  
def get_maximal_block(players_moves, remaining_moves):
    wins = gen_wins()
    score_list = [0 for x in range(NUMBER_OF_MOVES)]
    my_moves = tuple(x for x in range(NUMBER_OF_MOVES) if x not in players_moves + remaining_moves)
    for i in wins:
        #determine win sets containing a player token
        if set(i) - set(players_moves) != set(i) and\
           set(i) - set(my_moves) == set(i):
            for move in remaining_moves:
                if move in i:
                    score_list[move] += 1


    #print 'get_maxim', score_list, my_moves 
    #special case if opponent has chosen opposite corners your maximal block would be a corner
    #but you must play to win instead
    corners = (0,2,6,8)
    unused_corners = tuple(x for x in corners if x not in players_moves) 
    max_block = -1
    for x in range(NUMBER_OF_MOVES):
        if score_list[x] == max(score_list):
            #print 'YEAH', x
            max_block = x

    if max_block in corners and len(unused_corners) == 2:
        sides = (1,3,5,7)
        for x in remaining_moves:
            if x in sides:
                return x
    
    return max_block
        
  

def player_won(players_moves):
    #split this out for easier testing and reduction of duplication
    #TODO docstring
    #GM good candidate for class member
    wins = gen_wins()
    winning_state = False
    for i in wins:
        for j in itertools.combinations(players_moves, BOARD_SIZE):
            if set(i) - set(j)  == set(()):
                winning_state = True
    
    return winning_state
    

def has_won(current_state):
    '''
        returns: True if there is a winning state on the board for either player, False otherwise
        this is determined by comparing the odds and evens of the current_state. Those represent the moves
        made by a single player. Comparing the combinations of size three with the winning offsets will identify a win
    '''
     
    evens = tuple(current_state[i] for i in range(0, len(current_state), 2))
    odds  = tuple(current_state[i] for i in range(1, len(current_state), 2))

    return player_won(evens) or player_won(odds)

        
def choose_move(current_state, iter_count=0):

    #you can't win in the next transition if you only got one other token on the board
    #so introduce some special cases for opening moves
    corners = (0,2,6,8)

    #if len(current_state) in (0, 1):
    '''
    if set(corners) - set(current_state) == set(corners):
        return 0 
    
    else:
        remanin_corners = tuple(x for x in corners if x not in current_state)
        if len(remaning_corners):
            return remaning_corners[0]
    '''
    if 4 not in current_state:
        return 4
        

    remaining_moves = tuple(x for x in range(NUMBER_OF_MOVES) if x not in current_state) 

    #print remaining_moves, current_state

    if not len(remaining_moves):
        #GM TODO what does this really mean
        return

    if iter_count > len(remaining_moves):
        #GM if this works you need to define it better
        evens = tuple(current_state[i] for i in range(0, len(current_state), 2))
        #odds  = tuple(current_state[i] for i in range(1, len(current_state), 2))
        #snb = get_set_not_blocked(odds, remaining_moves)
        snb = get_maximal_block(evens, remaining_moves)
        return snb
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
    current_state = ()
    run_game(current_state)
