import copy

WHITE = 1
BLACK = 0
EMPTY_COLOR = -1

CORNERS_C = 4
EDGES_C = 2
CENTER_C = 3
F_RING_C = 2
S_RING_C = 1
BUFFERS_C = -1 

corners = [(0,0), (0,7), (7,0), (7,7)]

edges = [(0,2),(0,3),(0,4),(0,5),
         (2,0),(2,7),
         (3,0),(3,7),
         (4,0),(4,7),
         (5,0),(5,7),
         (7,2),(7,3),(7,4),(7,5)]

center = [(3,3),(4,3),(3,4),(4,4)]

first_ring = [(2,2),(2,3),(2,4),(2,5),
                (3,2),(3,5),
                (4,2),(4,5),
                (5,2),(5,3),(5,4),(5,5)
                ]

second_ring = [(1,2),(1,3),(1,4),(1,5),
                (2,1),(2,6),
                (3,1),(3,6),
                (4,1),(4,6),
                (5,1),(5,6),
                (6,2),(6,3),(6,4),(6,5)]

buffers = [(0,1),(1,0),(1,1),
           (0,6),(1,6),(1,7),
           (6,0),(6,1),(7,1),
           (6,7),(6,6),(7,6)]

board_parts = [corners, edges, center, first_ring, second_ring, buffers]
board_parts_costs = [CORNERS_C, EDGES_C, CENTER_C, F_RING_C, S_RING_C, BUFFERS_C]

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