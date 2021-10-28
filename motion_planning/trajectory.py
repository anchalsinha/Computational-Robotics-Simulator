import numpy as np
from chessboard import ChessboardEnvironment

# 0 - empty square
# 1 - obstacle
# G - goal state
board = np.array([
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 'G', 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
])
initial_state = (0, 0)
chessboard = ChessboardEnvironment(board, initial_state)
path = chessboard.rrt(10, (7, 7), 0.3)
print(path)