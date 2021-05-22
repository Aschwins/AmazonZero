import random
import numpy as np


class Actor:
    def __init__(self):
        pass
    
    def random_move(self, board):
        next_board_state = random.choice(board.next_board_states())
        return next_board_state

    def move(self, board, predictor, depth=1):
        is_whites_turn = board.is_whites_turn()
        next_board_states_flattened = \
            np.array([a.flatten() for a in board.next_board_states()])

        if is_whites_turn:
            class_idx = np.argwhere(predictor.model.classes_ == 1)[0][0]
        else:
            class_idx = np.argwhere(predictor.model.classes_ == 2)[0][0]

        y_pred, y_proba = predictor.predict(next_board_states_flattened)
        next_board_state_idx = np.argmax(y_proba[:, class_idx])
        next_board_state = (
            next_board_states_flattened[next_board_state_idx]
            .reshape(board.width, board.width)
        )

        # TODO: Check edge case. What if next_board_states is 1d??
        # TODO: This assumes the model has a classes_ attribute, which is 
        #       not always true.

        # TODO: Do monte carlo move sampling with additional depth
        return next_board_state

    
        
        
    
class Predictor:
    """
    The AmazonZero predictor class. 
    This class is used to predict which colors wins in a game of amazons.
    
    Params
    ------
    model (sklearn.BaseEstimator): 
    max_mem (int): Maximum number of rows in memory array
    memory (np.array): Array containing all games and results
    board_width
    
    """
    def __init__(self, model, max_mem=100_000, board_width=6, memory=None):
        self.model = model
        self.max_mem = max_mem
        self.board_width = board_width
        self.memory = memory or np.zeros((max_mem, board_width**2+1))
        self.mem_size = 0
        self.fitted = False
        
    def predict(self, boardstate):
        """
        Predicts the outcome of a boardstate of a game of amazons.

        Params
        ------
        boardstate (np.array): 1d array (flattened boardstate) to predict

        Returns
        -------
        y_pred (np.array): Predicted winner labels
        y_proba (np.array): Probability of predicted winner labels.
        """
        y_pred = self.model.predict(boardstate)
        y_proba = self.model.predict_proba(boardstate)
        return y_pred, y_proba
    
    def train(self):
        """
        Trains the predictor with all games in memory.
        """
        # grab only non empty rows to train on.
        Xy = self.memory[np.any(self.memory != 0, axis=1)]

        X, y = Xy[:, :-1], Xy[:, -1]
        self.model.fit(X, y)
        self.fitted = True
    
    def memorize(self, games):
        """
        Puts games in memory
        
        Params
        ------
        games (np.array): flattened board states over the rows with the 
                          result of the game in last column
        """
        n_lines = len(games)
        # Check wether we have enough memory left.
        enough_mem_left = (self.max_mem > (self.mem_size + n_lines))
        
        if not enough_mem_left:
            # shift the memory and overwrite
            mem_needed = self.mem_size + n_lines - self.max_mem
            self.memory = np.roll(self.memory, -1 * mem_needed, axis=0)
            self.mem_size -= mem_needed
            self.memory[self.mem_size:, :] = games
            
        else:
            self.memory[self.mem_size:self.mem_size + n_lines, :] = games
        
        self.mem_size += n_lines


class RandomPlayer:
    def __init__(self, actor):
        self.actor = actor

    def move(self, board):
        return self.actor.random_move(board)
    
class ForestPlayer:
    def __init__(self, predictor, actor):
        self.predictor = predictor
        self.actor = actor

    def move(self, board):
        return self.actor.move(board, self.predictor, depth=1)