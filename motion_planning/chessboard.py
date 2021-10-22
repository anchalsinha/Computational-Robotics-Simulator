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


    def a_star(self, start, end, actions):

        def h(end, next):
            # TODO: try manhattan distance
            return np.linalg.norm(end - next)

        from queue import PriorityQueue
        queue = PriorityQueue()
        queue.put(start, 0)
        came_from = {start: None}
        cost = {start: 0}

        while not queue.empty():
            current = queue.get()

            if current == end:
                return None

            for vertex in self.possible_jumps(actions, current):
                weight = 1 # TODO: Define weight of edge
                updated_cost = cost[current] + weight
                if vertex not in cost or updated_cost < cost[vertex]:
                    cost[vertex] = updated_cost
                    queue.put(vertex, updated_cost + h(end, vertex))
                    came_from[vertex] = current

        current = end
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)

        path.reverse()
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

    def p_norm(self, s1, s2, p=2):
        return np.linalg.norm(np.array(s1)-np.array(s2), p)

    def steer(self, s_rand, s_near):
        jumps = []
        one_jumps = [[s_near, s_next] for s_next in self.possible_jumps(self.A, s_near)]
        for one_jump in one_jumps:
            jumps.append(one_jump)
            next_jumps = self.possible_jumps(self.A, one_jump[-1])
            for next_jump in next_jumps:
                jumps.append(one_jump + [next_jump])

        min_dist = np.Inf
        best_jump = None

        for jump in jumps:
            curr_dist = self.p_norm(jump[-1], s_rand)
            if curr_dist < min_dist:
                min_dist = curr_dist
                best_jump = jump

        node1 = RRTVertex(best_jump[1], best_jump[0])
        if len(best_jump) > 2:
            node1.add_edge(best_jump[2])
            node2 = RRTVertex(best_jump[2], best_jump[1])

        # add nodes to rrt



    