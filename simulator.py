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

# def output(current state, grid)
#  return output probabilities
def output(state):
  dD = np.linalg.norm(state - Rd_loc)
  dS = np.linalg.norm(state - Rs_loc)
  h = 2/((1/dD) + (1/dS))
  o = [[np.ceil(h), 1 - (np.ceil(h) - h)], [np.floor(h), np.floor(h) - h]]
  

# def transition(current state, grid, action)
#  return next state

# main function for visuals/logging