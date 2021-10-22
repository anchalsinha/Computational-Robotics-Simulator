import numpy as np
import random

class RRTVertex:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.adjacent = []
    
    def add_edge(self, adjacent_state):
        self.adjacent.append(adjacent_state)

class ChessboardEnvironment:
    def __init__(self, board, initial_state):
        '''
        Define discrete state space system configuration from the defined grid. In the grid array,
        walls are defined as '1', empty spaces as '0'
        '''
        self.board = board
        self.initial_state = initial_state

        self.obstacle_coords = np.array(np.where(board == 1)).T
        self.rows, self.cols = board.shape

        # define state and action spaces
        self.S = [(y, x) for y in range(0, self.rows) for x in range(0, self.cols)]
        self.A = [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2)]
        self.graph = self.generate_graphs(self.S, self.A)
        self.visited = []
        self.queue = []

    def generate_graph(self, states, actions):
        graph = {}
        for state in states:
            graph[state] = self.possible_jumps(actions, state)
        return graph
    def bfs(self, visited, graph, node, queue):
        visited.append(node)
        queue.append(graph[node][:])
        path = []
        while queue:
            pass
        return path
    def possible_jumps(self, A, present_state):
        '''
        List all possible movements from the current state as to not select a wall or boundary as the 
        next state.
        '''
        possible_jumps= []
        for a in A:
            jump_y = present_state[0] + a[0]
            jump_x = present_state[1] + a[1]
            if jump_y >= 0 and jump_y < self.rows and jump_x >= 0 and jump_x < self.cols:
                if self.grid[jump_y, jump_x] != '1' and (self.grid[jump_y, jump_x] == '0' or np.array([jump_y, jump_x]) in self.target_coords):
                    possible_jumps.append((jump_y, jump_x))
        return possible_jumps
    def sample_board(self,present_state):
        
        sample_state = (random.randint(0,self.rows),random.randint(0,self.cols))

        return sample_state

    