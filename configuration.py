import numpy as np

# define state and action spaces
rows = 5
cols = 5
S = np.array([[x, y] for y in range(0, rows) for x in range(0, cols)])
A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1], [0, 0]])

# define P and O
P = None

O = {}
Rd_loc = [2, 2]
Rs_loc = [4, 2]
def output(state):
  dD = np.linalg.norm(state - Rd_loc)
  dS = np.linalg.norm(state - Rs_loc)
  h = 2/((1/dD) + (1/dS))
  o = [[np.ceil(h), 1 - (np.ceil(h) - h)], [np.floor(h), np.floor(h) - h]]

for s in S:
    O[tuple(s)] = output(s)