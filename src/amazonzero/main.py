import random
import tqdm
import numpy as np
import time

from sklearn.ensemble import RandomForestClassifier
from amazonzero.player import Predictor, Actor
from amazonzero.board import Board

def play_a_game(board, player1, player2, plot=False):
    turn = 0
    players = [player1, player2]

    end = False
    while not end:
        next_board = players[turn].move(board)
        turn = 1 - turn

        board.matrix = next_board
        end = board.check_if_ended()

    # print(board.matrix)
    # print(f"Winner is {board.winner}")
    if plot:
        board.plot_board()
    return board.winner


def main():
    # main loop to fill a Predictor memory with random games.
    n_generations = 8
    n_games = 500
    clf = RandomForestClassifier(max_depth=2, random_state=0)
    predictor = Predictor(clf, max_mem=100_000)
    epsilon = 0.5  # Explore vs Exploit

    for gen in range(n_generations):
        predictor = Predictor(predictor.model, max_mem=100_000)
        actor = Actor()
        
        for i in tqdm.trange(n_games, leave=True):
            board_states = []
            board = Board(6, 2)

            while not board.check_if_ended():
                # Explore
                if random.uniform(0,1) < epsilon:
                    next_board = actor.random_move(board)
                # Exploit
                else:
                    next_board = actor.move(board, predictor)
                board.matrix = next_board
                board_states.append(next_board.flatten())
                
            board_states = np.array(board_states)

            # append winner to the last column
            n_moves = len(board_states)
            y = np.zeros(n_moves) + 1 if board.winner == "white" else np.zeros(n_moves) + 2

            # create the feature matrix
            feature_matrix = np.concatenate([board_states, y.reshape(1, -1).T], axis=1)
            predictor.memorize(feature_matrix)
            
        predictor.train()