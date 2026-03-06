import sim_game_board as gb
from math import inf
import random

type Move = tuple[int, int]
type Direction = tuple[int, int]
type PlayerColor = int
type BoardState = list[list[int]]

DIRECTIONS: list[Direction] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
EMPTY_COLOR = -1
WHITE = 1
BLACK = 0
SURFACE = 3
MY_VALUES_W = 1 # weight of number of moves I can make in some state
OPP_VALUES_W = 0.5 # -|| - but opponent


def add(a: Move, b: Direction) -> Move:
    return (a[0] + b[0], a[1] + b[1])

class Node:
    def __init__(self, parent_move, max_fav = -inf, min_fav = inf, value = None):
        self.max_fav = max_fav
        self.min_fav = min_fav
        self.value = value
        self.parent_move = parent_move

    def __maximum__(self, other):
        if(self.value >= other.value): return self
        else: return other

    def __minimum__(self, other):
        if(self.value <= other.value): return self
        else: return other

class MyPlayer:
    """Player uses minimax and a-b pruning, manages to search to depth: 4"""

    # TODO replace docstring with a short description of your player

    def __init__(
        self, my_color: PlayerColor, opponent_color: PlayerColor, board_size: int = 8
    ):
        self.name = "kucerm59"
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size

    def minimax(self, board, parent_move, depth, max_fav, min_fav, maxPlayer) -> Node:
        # if exploartion ended
        if(depth == 0 or self.__is_game_over(board)):
            estimated_val = self.eval(board)
            #print("move: ", parent_move)
            return Node(parent_move,value=estimated_val)

        if maxPlayer:
            max_eval = Node((-1,-1), value= -inf)
            moves = self.get_all_valid_moves(board, self.my_color)
            for move in moves:
                new_board = gb.simulate_move(move, self.my_color, board)
                new_node = self.minimax(new_board, move, depth - 1, max_fav, min_fav, False)
                #print("options:", new_node.value, max_eval.value)
                max_eval = new_node.__maximum__(max_eval)
                #print("chosen max: ", max_eval.value)
                max_fav = max(max_fav, new_node.value)
                if min_fav <= max_fav:
                    break

            if(depth != SURFACE): max_eval.parent_move = parent_move
            return max_eval
        
        else:
            min_eval = Node((-1,-1), value= inf)
            moves = self.get_all_valid_moves(board, self.opponent_color)
            for move in moves:
                new_board = gb.simulate_move(move, self.opponent_color, board)
                new_node = self.minimax(new_board, move, depth-1, max_fav, min_fav, True)
                #print("options:", new_node.value, min_eval.value)
                min_eval = new_node.__minimum__(min_eval)
                #print("chosen min: ", min_eval.value )
                min_fav = min(min_fav, new_node.value)
                if min_fav <= max_fav:
                    break

            if(depth != SURFACE): min_eval.parent_move = parent_move
            return min_eval

    def __is_game_over(self, board: BoardState):
        if ((len(self.get_all_valid_moves(board, WHITE)) == 0) and \
               (len(self.get_all_valid_moves(board, BLACK)) == 0)):
            #print("Game is over")
            return True
        return False

    def get_board_cost(self, board: BoardState):
        """Calculates value of given board based on sections"""
        cost = 0
        for i in range(len(gb.board_parts)):
            for pos in gb.board_parts[i]:
                if(board[pos[0]][pos[1]] == self.my_color): cost += gb.board_parts_costs[i]
                elif(board[pos[0]][pos[1]] == self.opponent_color): cost -= gb.board_parts_costs[i]
        return cost
        
    def count_possible_moves(self, board):
        my_moves = len(self.get_all_valid_moves(board, self.my_color))
        opp_moves = len(self.get_all_valid_moves(board, self.opponent_color))
        result = (MY_VALUES_W * my_moves) - (OPP_VALUES_W * opp_moves)
        return result


    def eval(self, board: BoardState):
        """evaluates how good given state is"""
        e = self.get_board_cost(board)
        f = self.count_possible_moves(board)
        return e + f

    def select_move(self, board: BoardState) -> Move:
        #print("Dummy board: ",self.get_board_cost(gb.dummy_board), "\n\n")

        #moves = self.get_all_my_valid_moves(board)

        # print(moves, "\n")
        # for i in range(len(board)):
        #     print(board[i])
        # print("----------------------------------------------")
        best_node = self.minimax(board, None, SURFACE, -inf, inf, True )
        ##print(best_node.parent_move, best_node.value)
        # new_board = gb.simulate_move(moves[0],self.my_color, board)
        # for i in range(len(new_board)):
        #     print(new_board[i])

        # new_moves = self.get_all_valid_moves(new_board, self.opponent_color)
        # print("\n", new_moves)
        return best_node.parent_move

    def get_all_my_valid_moves(self, board: BoardState) -> list[Move]:
        """Get all valid moves for my player"""
        valid_moves: list[Move] = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                pos = (r, c)
                if self.__is_empty(pos, board) and self.__is_correct_move(pos, board, self.my_color):
                    valid_moves.append(pos)

        return valid_moves
    
    def get_all_valid_moves(self, board: BoardState, player_color) -> list[Move]:
        """Get all valid moves for selected player"""
        valid_moves: list[Move] = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                pos = (r, c)
                if self.__is_empty(pos, board) and self.__is_correct_move(pos, board, player_color):
                    valid_moves.append(pos)

        return valid_moves
    
    def __is_empty(self, pos: Move, board: BoardState) -> bool:
        """Check if the position is empty"""
        return board[pos[0]][pos[1]] == EMPTY_COLOR

    def __is_correct_move(self, move: Move, board: BoardState, player_color) -> bool:
        for step in DIRECTIONS:
            if self.__stones_flipped_in_direction(move, step, board, player_color) > 0:
                return True
        return False

    def __stones_flipped_in_direction(
        self, move: Move, step: Direction, board: BoardState, player_color
    ) -> int:
        """Check how many stones would be flipped in a given direction by a given player"""
        flipped_stones = 0
        if player_color == 1: opponent_color = 0
        else: opponent_color = 1
        
        pos = add(move, step)
        while self.__is_on_board(pos) and self.__stone_at(pos, board, opponent_color):
            flipped_stones += 1
            pos = add(pos, step)
        if not self.__is_on_board(pos):
            # Oponent's stones go all the way to the edge of the game board
            return 0
        if not self.__stone_at(pos, board, player_color):
            # There is not my stone at the end of opponent's stones
            return 0
        return flipped_stones

    def __my_stone_at(self, pos: Move, board: BoardState) -> bool:
        """Check if the position is occupied by me"""
        return board[pos[0]][pos[1]] == self.my_color

    def __opponent_stone_at(self, pos: Move, board: BoardState) -> bool:
        """Check if the position is occupied by the opponent"""
        return board[pos[0]][pos[1]] == self.opponent_color

    def __stone_at(self, pos: Move, board: BoardState, player_color) -> bool:
        """Check if the position is occupied by given player"""
        return board[pos[0]][pos[1]] == player_color

    def __is_on_board(self, pos: Move) -> bool:
        """Check if the position exists on the board"""
        return 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size
