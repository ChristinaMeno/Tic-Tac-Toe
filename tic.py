#!/usr/bin/env python
import itertools

'''
GM: this is how the tuple that represents board state is organized
    current_state = (0, 8, 4,) represents a game in which three moves have been made
    currently odd moves are marked by an X and even moves are O. Each element of the tuple
    is an index on the board layout below.

    0 1 2
    3 4 5
    6 7 8
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
        

def gen_wins():
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

  
def get_maximal_block(opponent_moves, remaining_moves):
    '''
        returns: The next move which blocks the most of opponents moves.
    '''
    wins = gen_wins()
    score_list = [0 for x in range(NUMBER_OF_MOVES)]
    my_moves = tuple(x for x in range(NUMBER_OF_MOVES) if x not in opponent_moves + remaining_moves)
    for i in wins:
        #determine win sets containing a opponent tokens and which sets we don't have a token in.
        if set(i) - set(opponent_moves) != set(i) and\
           set(i) - set(my_moves) == set(i):
            for move in remaining_moves:
                if move in i:
                    score_list[move] += 1


    #this is looking for which move is a member of a winning set 
    #that satisfies the rules above with the highest frequency
    max_block = score_list.index(max(score_list)) 
    
    #special case if opponent has chosen opposite corners your maximal block would be a corner
    #but you must play to win instead
    corners = (0,2,6,8)
    unused_corners = tuple(x for x in corners if x not in opponent_moves) 
    if max_block in corners and len(unused_corners) == 2:
        sides = (1,3,5,7)
        for x in remaining_moves:
            if x in sides:
                return x
    
    return max_block
  

def player_won(players_moves):
    '''
        returns: True if there is a winning state in players moves, False otherwise.
        For this to be useful players moves should be a sequence of even moves or odd moves
    '''
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

        
def choose_move(current_state, computer_first=False, iter_count=0):
    '''
        returns: Computers choice for next move.
    '''
    #special cases for opening move
    if 4 not in current_state:
        return 4
        
    remaining_moves = tuple(x for x in range(NUMBER_OF_MOVES) if x not in current_state) 

    #recursion base case
    if iter_count > len(remaining_moves):
        opponent_moves = tuple(current_state[i] for i in range(int(computer_first), len(current_state), 2))
        return get_maximal_block(opponent_moves, remaining_moves)

    #choose a wining move for computer
    for x in remaining_moves:
        next_state = current_state + (x,) 
        if has_won(next_state):
            return x 

    #choose no state, and see if the next move could be a win
    return choose_move(current_state + (-1,), computer_first, iter_count + 1)


def run_game(current_state):
    '''
        Displays available move to choose
        Interactively asks human player for a move
        draws boards and determines winner
    ''' 
    draw_board(current_state)
    
    #human plays the even moves
    human_plays = 1
    current_player = 'computer'

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
            next_move = choose_move(current_state, human_plays)

        #update state and draw_board
        current_state = current_state + (next_move,) 
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
