import random


class RandomPlayer:
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def move(self):
        # grab a white piece
        pieces = self.board.get_pieces(self.color)
        options = []  # (piece, option)

        for piece in pieces:
            matrix = self.board.matrix
            options += [[piece, opt] for opt in self.board.get_options(matrix, piece)]

        choice = random.choice(options)
        self.board.move(choice[0], choice[1])

        # shoot
        shoot_options = self.board.get_options(self.board.matrix, choice[1])
        shoot_choice = random.choice(shoot_options)
        self.board.shoot(shoot_choice)
