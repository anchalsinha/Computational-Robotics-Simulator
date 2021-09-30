import numpy as np

# define state and action spaces
rows = 5
cols = 5
S = np.array([[x, y] for y in range(0, rows) for x in range(0, cols)])
A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1], [0, 0]])

# define P and O
P = None
O = None