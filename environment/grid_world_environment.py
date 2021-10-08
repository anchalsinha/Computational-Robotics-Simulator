import numpy as np

from .base_environment import Environment

class GridworldEnvironment(Environment):
    def __init__(self, grid, Pe):
        '''
        Define discrete state space system configuration from the defined grid. In the grid array,
        walls are defined as '1', empty spaces as '0', and targets as a characters ('D' and 'S')
        '''
        self.grid = grid
        self.Pe = Pe

        self.target_coords = np.array(np.where((grid != '0') & (grid != '1'))).T
        print(self.target_coords)
        self.rows, self.cols = grid.shape

        # define state and action spaces
        S = [(y, x) for y in range(0, self.rows) for x in range(0, self.cols)]
        A = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]

        O = self.calculate_observation_set(S)
        P = self.calculate_transition_prob_set(S, A)

        R = self.calculate_reward_set(S, A)

        Environment.__init__(self, S, A, P, O, R)

    def calculate_reward_set(self, S, A):
        R = {}
        for state in S:
            for action in A:
                for next_state in S:
                    R.setdefault(state, {})
                    R[state].setdefault(action, {})
                    R[state][action][next_state] = 1 if self.grid[next_state] == 'D' or self.grid[next_state] == 'H' else 0

    def calculate_observation_set(self, S):
        O = {}
        for state in S:
            h = np.mean(np.linalg.norm(np.subtract(self.target_coords, state), axis=1))
            o = np.array([[np.ceil(h), 1 - (np.ceil(h) - h)], [np.floor(h), np.ceil(h) - h]])
            O[state] = o
        return O

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

    def calculate_transition_prob_set(self, S, A):
        '''
        Calculates the transition probability set. The data type is a triple-nested dictionary to 
        represent the input triplet (state, action, next state) determining the transition probability
        '''
        transition_mat = {}
        for s in S: # current state
            if self.grid[s] == '1':
                continue

            list_possible_jumps = self.possible_jumps(A, s)
            a_dic ={}

            for a in A: # current action
                s_dict = {}
                desired_state = tuple(np.add(s, a))
                invalid = tuple(desired_state) not in list_possible_jumps # check if desired state is invalid

                for s_ in S: # next state
                    if invalid and s_ == s: # if invalid desired state and s_ is current state
                        s_dict[s_] = 1
                    elif not invalid and desired_state == s_: # if not invalid desired state and s_ is desired state
                        s_dict[s_] = float(1-self.Pe)
                    elif not invalid and s_ in list_possible_jumps: # if not invalid desired state and s_ is valid
                        s_dict[s_] = self.Pe/(len(list_possible_jumps)-1)
                    else:
                        s_dict[s_] = 0
                a_dic[a]= s_dict
            transition_mat[tuple(s)]  = a_dic
        return transition_mat
    