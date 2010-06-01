import tic

def test_has_won():
    #TEST ODDS and EVENS in has_won()
    for x in range(tic.NUMBER_OF_MOVES):
        current_state = tuple(xrange(x))
        tic.has_won(current_state)

def choose_all_moves(current_state, start_game=0):
    remaining_moves = tuple(x for x in range(tic.NUMBER_OF_MOVES) if x not in current_state) 
    
    #if the computer wins first dont keep looking at this state
    my_moves = tuple(current_state[i] for i in range(start_game, len(current_state), 2))
    comp_moves = tuple(x for x in current_state if x not in my_moves) 
    if tic.player_won(comp_moves):
        return 
 
    #base case check
    if len(current_state) == tic.NUMBER_OF_MOVES:
        if tic.player_won(my_moves):
            print 'OOPS', current_state, my_moves, comp_moves

    #we play the opening move? 
    if len(current_state) % 2 == start_game:
        for next_move in remaining_moves:
            choose_all_moves(current_state + (next_move,))
    else:
        next_move = tic.choose_move(current_state) 
        if next_move != None:
            choose_all_moves(current_state + (next_move,))
            
            
        
        
if __name__ == '__main__':
    current_state = ()
    tic.draw_board(current_state)
    print 'losing games where Human goes first'
    choose_all_moves(current_state)
    print 'losing games where Computer goes first'
    choose_all_moves(current_state, 1)
