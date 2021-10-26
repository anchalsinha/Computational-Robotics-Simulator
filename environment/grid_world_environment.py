import numpy as np

from .base_environment import Environment

class GridworldEnvironment(Environment):
    def __init__(self, grid, Pe):
        '''
        Define discrete state space system configuration from the defined grid. In the grid array,
        walls are defined as '1', empty spaces as '0', targets as characters ('D' and 'S'), and 
        roads as character 'W', 
        '''
        # define problem-specific parameters
        self.grid = grid
        self.Pe = Pe

        self.target_coords = np.array(np.where((grid == 'D') | (grid == 'S'))).T
        self.road_coords = np.array(np.where((grid == 'W'))).T
        self.reward_coords = np.concatenate([self.target_coords, self.road_coords])
        self.rows, self.cols = grid.shape

        # define state and action spaces
        S = [(y, x) for y in range(0, self.rows) for x in range(0, self.cols)]
        A = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]

        O = self.calculate_observation_set(S)
        P = self.calculate_transition_prob_set(S, A)

        R = self.calculate_reward_set(S, A)

        Environment.__init__(self, S, A, P, O, R)

    def calculate_reward_set(self, S, A):
        '''
        Initialize R for all (state, action, next state) triplets as a triple-nested dictionary
        '''
        R = {}
        for state in S:
            for action in A:
                for next_state in S:
                    R.setdefault(state, {})
                    R[state].setdefault(action, {})
                    if list(next_state) in self.target_coords.tolist():
                        R[state][action][next_state] = 1
                    elif list(next_state) in self.road_coords.tolist():
                        R[state][action][next_state] = -1
                    else:
                        R[state][action][next_state] = 0
        return R

    def calculate_observation_set(self, S):
        '''
        Initialize O for all s in S as a dictionary
        '''    
        O = {}
        for state in S:
            h = np.mean(np.linalg.norm(np.subtract(self.target_coords, state), axis=1))
            o = np.array([[np.ceil(h), 1 - (np.ceil(h) - h)], [np.floor(h), np.ceil(h) - h]])
            O[state] = o
        return O

    def possible_jumps(self, A, present_state):
        '''
        Return all possible next states from the current state as to not select a wall or boundary as the 
        next state.
        '''
        possible_jumps = []
        for a in A:
            jump_y = present_state[0] + a[0]
            jump_x = present_state[1] + a[1]
            if jump_y >= 0 and jump_y < self.rows and jump_x >= 0 and jump_x < self.cols:
                if self.grid[jump_y, jump_x] != '1' and (self.grid[jump_y, jump_x] == '0' or np.array([jump_y, jump_x]) in self.target_coords):
                    possible_jumps.append((jump_y, jump_x))
        return possible_jumps

    def possible_actions(self, present_state):
        '''
        Return all possible actions for all next states in the set of possible next states (aka possible_jumps)
        '''
        return [(next_state[0] - present_state[0], next_state[1] - present_state[1]) for next_state in self.possible_jumps(self.A, present_state)]

    def calculate_transition_prob_set(self, S, A):
        '''
        Calculates the transition probability set. The data type is a triple-nested dictionary to 
        represent the input triplet (state, action, next state) determining the transition probability
        '''
        transition_prob_dict = {}
        for s in S: # current state
            if self.grid[s] == '1':
                continue

            possible_jumps_list = self.possible_jumps(A, s)
            a_dict = {}

            for a in A: # current action
                s_dict = {}
                desired_state = tuple(np.add(s, a))
                invalid = desired_state not in possible_jumps_list # check if desired state is invalid

                for s_ in S: # next state
                    s_dict[s_] = self.assign_prob(s, s_, invalid, desired_state, possible_jumps_list)

                a_dict[a] = s_dict
            transition_prob_dict[tuple(s)] = a_dict
        return transition_prob_dict
    
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
                row += f'{self.get_reward((0,0),(0,0),(i, j))}|'
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

    def assign_prob(self, state, next_state, invalid, desired_state, possible_jumps_list):
        '''
        Assign probability of transitioning from state to next state having determined the desired next state for 
        a given state action tuple. The validity of the desired next state is given by input (invalid) and 
        possible_jumps_list contains a list of all possible valid transitions that can occur from state 
        '''
        if invalid and state == next_state: # if invalid desired state and s_ is current state
            return 1
        elif not invalid and desired_state == next_state: # if not invalid desired state and s_ is desired state
            return float(1 - self.Pe)
        elif not invalid and next_state in possible_jumps_list: # if not invalid desired state and s_ is valid
            return self.Pe/(len(possible_jumps_list)-1)
        else:
            return 0

    def get_prob(self, state, action, next_state):
        '''
        Return the probability of transitioning to next state given state and action
        '''
        possible_jumps_list = self.possible_jumps(self.A, state)
        desired_state = tuple(np.add(state, action))
        invalid = desired_state not in possible_jumps_list

        return self.assign_prob(state, next_state, invalid, desired_state, possible_jumps_list)

    def get_reward(self, state, action, next_state):
        '''
        Return the reward for the input triplet (state, action, next state) 
        '''      
        return self.R[state][action][next_state]