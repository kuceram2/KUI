import copy


"""Helper module for MiniMax search,
functions adapted from game_board.py"""
WHITE = 1
BLACK = 0
EMPTY_COLOR = -1

CORNERS_C = 4
EDGES_C = 2
CENTER_C = 3
F_RING_C = 2
S_RING_C = 1
T_RING_C = 2
BUFFERS_C = -1 

corners_8 = [(0,0), (0,7), (7,0), (7,7)]
corners_6 = [(0,0), (0,5), (5,0), (5,5)]
corners_10 = [(0,0), (0,9), (9,0), (9,9)]

edges_8 = [(0,2),(0,3),(0,4),(0,5),
         (2,0),(2,7),
         (3,0),(3,7),
         (4,0),(4,7),
         (5,0),(5,7),
         (7,2),(7,3),(7,4),(7,5)]

edges_6 = [(0,2),(0,3),
         (2,0),(2,5),
         (3,0),(3,5),
         (5,2),(5,3)]

edges_10 = [(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
         (2,0),(2,9),
         (3,0),(3,9),
         (4,0),(4,9),
         (5,0),(5,9),
         (6,0),(6,9),
         (7,0),(7,9),
         (9,2),(9,3),(9,4),(9,5),(9,6),(9,7)]

center_8 = [(3,3),(4,3),(3,4),(4,4)]
center_6 = [(2,2),(2,3),(3,2),(3,3)]
center_10 = [(4,4),(4,5),(5,4),(5,5)]

first_ring_8 = [(2,2),(2,3),(2,4),(2,5),
                (3,2),(3,5),
                (4,2),(4,5),
                (5,2),(5,3),(5,4),(5,5)]

first_ring_6 = [(1,2),(1,3),
                (2,1),(2,4),
                (3,1),(3,4),
                (4,2),(4,3)]

first_ring_10 = [(3,3),(3,4),(3,5),(3,6),
                (4,3),(4,6),
                (5,3),(5,6),
                (6,3),(6,4),(6,5),(6,6)]

second_ring_8 = [(1,2),(1,3),(1,4),(1,5),
                (2,1),(2,6),
                (3,1),(3,6),
                (4,1),(4,6),
                (5,1),(5,6),
                (6,2),(6,3),(6,4),(6,5)]

second_ring_10 = [(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),
                (3,2),(3,7),
                (4,2),(4,7),
                (5,2),(5,7),
                (6,2),(6,7),
                (7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]

third_ring_10 = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
         (2,1),(2,8),
         (3,1),(3,8),
         (4,1),(4,8),
         (5,1),(5,8),
         (6,1),(6,8),
         (7,1),(7,8),
         (8,2),(8,3),(8,4),(8,5),(8,6),(8,7)]

buffers_8 = [(0,1),(1,0),(1,1),
           (0,6),(1,6),(1,7),
           (6,0),(6,1),(7,1),
           (6,7),(6,6),(7,6)]

buffers_6 = [(0,1),(1,0),(1,1),
           (0,4),(1,4),(1,5),
           (4,0),(4,1),(5,1),
           (5,4),(4,4),(4,5)]

buffers_10 = [(0,1),(1,0),(1,1),
           (0,8),(1,8),(1,9),
           (8,0),(8,1),(9,1),
           (8,9),(8,8),(9,8)]

board_parts = {
    10: [corners_10, edges_10, center_10, first_ring_10, second_ring_10, third_ring_10, buffers_8],
    8: [corners_8, edges_8, center_8, first_ring_8, second_ring_8, buffers_8],
    6: [corners_6, edges_6, center_6, first_ring_6, buffers_6]
}
board_parts_costs = {
     10: [CORNERS_C, EDGES_C, CENTER_C, F_RING_C, S_RING_C, T_RING_C, BUFFERS_C],
     8: [CORNERS_C, EDGES_C, CENTER_C, F_RING_C, S_RING_C, BUFFERS_C],
     6: [CORNERS_C, EDGES_C, CENTER_C, F_RING_C, BUFFERS_C]
     }

dummy_board = [ [1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [0, -1, 0, -1, -1, -1, -1, -1]]


def simulate_move(move, players_color, board):
        '''
        returns resulting board after a given move made by given player
        :param move: position where the move is made [x,y]
        :param player: player that made the move
        '''
        new_board = copy.deepcopy(board)
        new_board[move[0]][move[1]] = players_color
        dx = [-1,-1,-1,0,1,1,1,0]
        dy = [-1,0,1,1,1,0,-1,-1]
        for i in range(len(dx)):
            if confirm_direction(move,dx[i],dy[i],players_color, new_board):
                change_stones_in_direction(move, dx[i], dy[i], players_color, new_board)
        return new_board

def confirm_direction(move,dx,dy,players_color, board):
        '''
        Looks into dirextion [dx,dy] to find if the move in this dirrection is correct.
        It means that first stone in the direction is oponents and last stone is players.
        :param move: position where the move is made [x,y]
        :param dx: x direction of the search
        :param dy: y direction of the search
        :param player: player that made the move
        :return: True if move in this direction is correct
        '''
        if players_color == WHITE:
            opponents_color = BLACK
        else:
            opponents_color = WHITE
        board_size = len(board)

        posx = move[0]+dx
        posy = move[1]+dy
        if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
            if board[posx][posy] == opponents_color:
                while (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < board_size) and (posy >= 0) and (posy < board_size):
                        if board[posx][posy] == EMPTY_COLOR:
                            return False
                        if board[posx][posy] == players_color:
                            return True

        return False

def change_stones_in_direction(move, dx, dy, players_color, board):
    posx = move[0]+dx
    posy = move[1]+dy
    while (not(board[posx][posy] == players_color)):
        board[posx][posy] = players_color
        posx += dx
        posy += dy