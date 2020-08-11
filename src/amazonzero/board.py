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

    def get_options(self, from_sq):
        row = from_sq[0]
        col = from_sq[1]
        options = []

        # to the right
        for j in range(col + 1, self.width):
            if self.matrix[row][j] == 0:
                options.append([row, j])
            else:
                break

        # to the left
        for j in range(col - 1, -1, -1):
            if self.matrix[row][j] == 0:
                options.append([row, j])
            else:
                break

        # down
        for i in range(row + 1, self.width):
            if self.matrix[i][col] == 0:
                options.append([i, col])
            else:
                break

        # up
        for i in range(row - 1, -1, -1):
            if self.matrix[i][col] == 0:
                options.append([i, col])
            else:
                break

        # upleft
        for offset in range(1, min(row, col) + 1):
            if self.matrix[row - offset][col - offset] == 0:
                options.append([row - offset, col - offset])
            else:
                break

        # upright
        for offset in range(1, min(row, self.width - col - 1) + 1):
            if self.matrix[row - offset][col + offset] == 0:
                options.append([row - offset, col + offset])
            else:
                break

        # downleft
        for offset in range(1, min(self.width - row - 1, col) + 1):
            if self.matrix[row + offset][col - offset] == 0:
                options.append([row + offset, col - offset])
            else:
                break

        # downright
        for offset in range(1, min(self.width - row - 1, self.width - col - 1) + 1):
            if self.matrix[row + offset][col + offset] == 0:
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
            if len(self.get_options(piece)) > 0:
                return False

        self.winner = "white" if self.turn == "black" else "black"
        return True

    def next_board_states(self):
        pass


class RandomPlayer:
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def move(self):
        # grab a white piece
        pieces = self.board.get_pieces(self.color)
        options = []  # (piece, option)

        for piece in pieces:
            options += [[piece, opt] for opt in self.board.get_options(piece)]

        choice = random.choice(options)
        self.board.move(choice[0], choice[1])

        # shoot
        shoot_options = self.board.get_options(choice[1])
        shoot_choice = random.choice(shoot_options)
        self.board.shoot(shoot_choice)


def play_a_game(board, player1, player2):
    turn = 0
    players = [player1, player2]

    end = False
    while not end:
        players[turn].move()
        turn = 1 - turn

        end = board.check_if_ended()

    print(board.matrix)
    print(f"Winner is {board.winner}")
    board.plot_board()
