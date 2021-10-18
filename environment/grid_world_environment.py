import numpy as np
import itertools

from .base_environment import Environment

class GridworldEnvironment(Environment):
    def __init__(self, grid, Pe, n_agents):
        '''
        Define discrete state space system configuration from the defined grid. In the grid array,
        walls are defined as '1', empty spaces as '0', and targets as a characters ('D' and 'S')
        '''
        self.grid = grid
        self.Pe = Pe

        self.target_coords = np.array(np.where((grid == 'D') | (grid == 'S'))).T
        self.road_coords = np.array(np.where((grid == '2'))).T
        self.rows, self.cols = grid.shape

        # define state and action spaces
        coords = list(map(tuple, np.mgrid[0:5,0:5].T.reshape(-1, 2)))
        S = list(itertools.product(coords, repeat=n_agents))
        actions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        A = list(itertools.product(actions, repeat=n_agents))

        # O = self.calculate_observation_set(S)
        # P = self.calculate_transition_prob_set(S, A)

        # R = self.calculate_reward_set(S, A)

        Environment.__init__(self, S, A, None, None, None)

    def subtract_coords(self, state, target):
        return np.array([target - s for s in state]).reshape(-1, 2)

    def calculate_phi(self, state):
        basis_functions = [
            np.sum(np.linalg.norm(state, axis=1)), # sum of distances 
            np.sum([np.mean(np.linalg.norm(self.subtract_coords(s, self.target_coords), axis=1)) for s in state]), # sum of harmonic mean distance to targets
            np.sum([np.mean(np.linalg.norm(self.subtract_coords(s, self.road_coords), axis=1)) for s in state]), # sum of harmonic mean distance to the road
        ]
        basis_functions += [len(self.possible_jumps(self.A, s)) for s in state] # number of possible jumps for each agent

        return basis_functions

    def possible_jumps(self, A, present_state):
        '''
        List all possible movements from the current state as to not select a wall or boundary as the 
        next state.
        '''
        possible_jumps= []
        for a in A:
            jump_state = np.add(present_state, a)
            valid = True
            for s in jump_state:
                if s[0] >= 0 and s[0] < self.rows and s[1] >= 0 and s[1] < self.cols:
                    valid &= self.grid[tuple(s)] != '1' and (self.grid[tuple(s)] == '0' or s in self.target_coords)
            if valid:
                possible_jumps.append(jump_state)

        return possible_jumps

    def calculate_transition_prob(self, state, action):
        '''
        Calculates the transition probabilities for the surrounding next states provided the current state and action. 
        Instead of calculating the complete set P acting as a "lookup table", we will compute the transition probabilities 
        for every transition when needed to make it robust to situations when the state space is very large.
        '''
        list_possible_jumps = self.possible_jumps(self.A, state)
        next_states = np.add(self.A, state)
        desired_state = np.add(action, state)
        invalid = np.equal(desired_state, list_possible_jumps).all(axis=1).any() # check if desired state is invalid

        P = {}

        for s in next_states: # next state
            key = tuple(map(tuple, s))
            if invalid and np.array_equal(s, np.array(state)): # if invalid desired state and s_ is current state
                P[key] = 1
            elif not invalid and np.array_equal(s, desired_state): # if not invalid desired state and s is desired state
               P[key] = float(1-self.Pe)
            elif not invalid and s in list_possible_jumps: # if not invalid desired state and s is valid
                P[key] = self.Pe/(len(list_possible_jumps)-1)
            else:
                P[key] = 0

        return P
    
    def calculate_reward(self, state):
        if list(state) in self.target_coords.tolist():
            return 1
        elif list(state) in self.road_coords.tolist():
            return -1
        else:
            return 0

    def calculate_observation(self, state):
        h = np.mean(np.linalg.norm(self.subtract_coords(state, self.target_coords), axis=1))
        return np.array([[np.ceil(h), 1 - (np.ceil(h) - h)], [np.floor(h), np.ceil(h) - h]])

    def visualize(self, states, policy):
        print("Policy: ")
        for i in range(len(self.grid)):
            row = '|'
            for j in range(len(self.grid[0])):
                if policy[i, j] == (0, 0):
                    row += 'S|'
                elif policy[i, j] == (1, 0):
                    row += '↓|'
                elif policy[i, j] == (-1, 0):
                    row += '↑|'
                elif policy[i, j] == (0, 1):
                    row += '→|'
                else:
                    row += f'←|'
            print(row)

        print("Reward: ")
        for i in range(len(self.grid)):
            row = '|'
            for j in range(len(self.grid[0])):
                row += f'{self.get_r((0,0),(0,0),(i, j))}|'
            print(row)

        for i in range(len(self.grid)):
            row = '|'
            for j in range(len(self.grid[0])):
                if (i, j) in states:
                    row += 'O|'
                elif self.grid[i, j] == '0':
                    row += '_|'
                elif self.grid[i, j] == '1':
                    row += 'X|'
                else:
                    row += f'{self.grid[i, j]}|'
            print(row)

        print('\n\n\n')
