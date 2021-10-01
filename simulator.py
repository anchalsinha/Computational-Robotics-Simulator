import numpy as np
import matplotlib.pyplot as plt
from configuration import S, A, P, O

# define grid
grid = np.array([
        [0, 0, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 'D', 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 'S', 0, 1],
])
Rd_loc = list(zip(*np.where(grid == 'D')))[0]
Rs_loc = list(zip(*np.where(grid == 'S')))[0]

state = [0, 2]

def selectAction():
    pass

def takeAction(action):
    pass

# main function for visuals/logging