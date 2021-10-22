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
path = chessboard.bfs(graph=chessboard.graph, node=initial_state)
print(path)
chessboard.visualize(board,path)