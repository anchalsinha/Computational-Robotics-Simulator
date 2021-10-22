import numpy as np

class ChessboardEnvironment:
    def __init__(self, board):
        '''
        Define discrete state space system configuration from the defined grid. In the grid array,
        walls are defined as '1', empty spaces as '0'
        '''
        self.board = board

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
    def backtrace(self,start_node,end_node, parents):
        path = []
        current_node = end_node
        while current_node is not start_node:
            path.append(parents[current_node])
            current_node = parents[current_node]

        return path
    def bfs(self, graph, node):
        queue = []
        visited = []
        parent = {}
        queue.append(node)
        while queue:
            current_node = queue.pop()
            if self.board[current_node]  == 'G':
                return self.backtrace(node,current_node, parent )
            else:
                neighbours = graph[current_node]
                for n in neighbours:
                    if n not in visited:
                        parent[n] = current_node
                        queue.append(n)
                        visited.append(n)
        return []

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
