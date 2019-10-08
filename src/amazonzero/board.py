import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

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
        
    def create_board(self):
        matrix = np.zeros(shape=(self.width, self.width))
        for i in range(self.n_amazons):
            matrix[i][i] = 1
            matrix[self.width-i-1][self.width-i-1] = 2
        return matrix
    
    def plot_board(self):
        plt.imshow(self.matrix, cmap=ListedColormap(['white', 'beige', 'black', 'red']), interpolation='nearest')
        plt.axis("off")
        plt.show()