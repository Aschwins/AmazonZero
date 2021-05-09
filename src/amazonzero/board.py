import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap

TURN = ['white', 'black']

colormap = {'white': 1, 'black': 2}


class Board:
    """
    A board class of width x width with n_amazons for each side.
    """

    def __init__(self, width, n_amazons):
        if width / n_amazons < 2:
            raise ValueError("Not enough room for the Amazons. Use less amazons our create a bigger board.")
        self.width = width
        self.n_amazons = n_amazons
        self.matrix = self.create_board()
        self.turn = 'white'
        self.winner = None

    def create_board(self):
        matrix = np.zeros(shape=(self.width, self.width))
        for i in range(self.n_amazons):
            matrix[i][i] = 1
            matrix[self.width - i - 1][self.width - i - 1] = 2
        return matrix

    def plot_board(self):
        plt.imshow(self.matrix, cmap=ListedColormap(['white', 'beige', 'black', 'red']))
        plt.axis("off")
        plt.show()

    def available_squares(self, color='white'):
        """
        Calculates the number of available squares.


        :param color:
        :return:
        """
        pass

    def get_options(self, matrix, from_sq):
        row = from_sq[0]
        col = from_sq[1]
        width = len(matrix)  # Square boards only!!!
        options = []

        # to the right
        for j in range(col + 1, width):
            if matrix[row][j] == 0:
                options.append([row, j])
            else:
                break

        # to the left
        for j in range(col - 1, -1, -1):
            if matrix[row][j] == 0:
                options.append([row, j])
            else:
                break

        # down
        for i in range(row + 1, width):
            if matrix[i][col] == 0:
                options.append([i, col])
            else:
                break

        # up
        for i in range(row - 1, -1, -1):
            if matrix[i][col] == 0:
                options.append([i, col])
            else:
                break

        # upleft
        for offset in range(1, min(row, col) + 1):
            if matrix[row - offset][col - offset] == 0:
                options.append([row - offset, col - offset])
            else:
                break

        # upright
        for offset in range(1, min(row, width - col - 1) + 1):
            if matrix[row - offset][col + offset] == 0:
                options.append([row - offset, col + offset])
            else:
                break

        # downleft
        for offset in range(1, min(width - row - 1, col) + 1):
            if matrix[row + offset][col - offset] == 0:
                options.append([row + offset, col - offset])
            else:
                break

        # downright
        for offset in range(1, min(width - row - 1, width - col - 1) + 1):
            if matrix[row + offset][col + offset] == 0:
                options.append([row + offset, col + offset])
            else:
                break

        return options

    def next_turn(self):
        "Sets the board to the next turn"

        ix = TURN.index(self.turn)
        next_turn = TURN[(ix + 1) % 2]
        self.turn = next_turn

    def move(self, from_sq, to_sq):
        piece = self.matrix[from_sq[0], from_sq[1]]
        self.matrix[from_sq[0], from_sq[1]] = 0
        self.matrix[to_sq[0], to_sq[1]] = piece

    def shoot(self, sq):
        self.matrix[sq[0], sq[1]] = 3
        self.next_turn()

    def get_pieces(self, color):
        pieces = [[i, j] for i in range(0, self.width) for j in range(0, self.width) \
                  if self.matrix[i][j] == colormap.get(color)]
        return pieces

    def check_if_ended(self):
        pieces = self.get_pieces(self.turn)
        for piece in pieces:
            if len(self.get_options(self.matrix, piece)) > 0:
                return False

        self.winner = "white" if self.turn == "black" else "black"
        return True

    def next_board_states(self):
        """
        Give a board state (matrix), calculates all the possible next board states
        """
        n_fires = np.sum(self.matrix == 3)
        whites_turn = ((n_fires % 2) == 0)

        if whites_turn:
            pieces = [[i, j] for i, j in zip(range(0, self.width),range(0, self.width)) if self.matrix[i][j] == 1]
        else:
            pieces = [[i, j] for i, j in zip(range(0, self.width),range(0, self.width)) if self.matrix[i][j] == 2]

        boards = []
        for p in pieces:
            options_step1 = self.get_options(self.matrix, p)
            mv_boards_p = self.get_move_boards(self.matrix, p, options_step1)
            for j, mv_board in enumerate(mv_boards_p):
                options_step2 = self.get_options(mv_board, options_step1[j])
                shoot_boards = self.get_shoot_boards(mv_board, options_step2)
                boards += shoot_boards
        return boards

    def get_move_boards(self, matrix, p, piece_options):
        boards = []
        color = matrix[p[0], p[1]]
        for opt in piece_options:
            new_board = matrix.copy()
            new_board[p[0], p[1]] = 0
            new_board[opt[0], opt[1]] = color
            boards.append(new_board)
            
        return boards
            
    def get_shoot_boards(self, matrix, shoot_options):
        boards = []
        for opt in shoot_options:
            new_board = matrix.copy()
            new_board[opt[0], opt[1]] =3
            boards.append(new_board)
        return boards
