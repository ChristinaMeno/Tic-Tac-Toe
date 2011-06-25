import tic
import json

tic.draw_board((0,1,2,3,4,5,6,7,8), True)

tic.draw_board((4, 0, 1, 7,))
print json.dumps(dict(sha1='44475cf57725c5a988a27cebe6e79a8bbf732f85', game_state=(4, 0, 1, 7, 3,)))
tic.draw_board((4, 0, 1, 7,3))
tic.draw_board((4, 0, 1, 7, 3, 5, 2, 6, 8))
