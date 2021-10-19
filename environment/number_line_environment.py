import numpy as np
import random
from scipy.misc import derivative

from .base_environment import Environment

class NumberLineEnvironment(Environment):
    def __init__(self,gamma = 0.8,hill_size=2,resolution=0.1):
        # TODO: Define S, A, P, and O
        # Environment.__init__(self, S, A, P, O)
        self.v_max = 10
        self.y_max = 10
        self.p_c = 5
        self.m = 10
        self.hill_size = hill_size    #TODO make input

        #MDP
        self.gamma = gamma
        self.resolution = resolution

        self.position = 0  # position
        self.velocity = 0  # velocity
        self.time = 0
        


        self.state_space_discretization(self.resolution) # sets the position_space and velocity_space
        self.update_state()

        # define state and action spaces.We formulate based on aggregate sets
        S = [(y, x) for y in self.position_space for x in  self.velocity_space]  # set of all states
        A = [-1,0,1]                                   # set of all actions

        O = self.calculate_observation_set(S)            # set of all observations 
        P = self.calculate_transition_prob_set(S, A)    # set of all transtions probabilities
        R = self.calculate_reward_set(S,A)

        Environment.__init__(self, S, A, P, O,R)
    
    def state_space_discretization(self,resolution= 0.1):
        self.position_space = np.array([a for a in range(-self.y_max,self.y_max,resolution)])
        self.velocity_space = np.array([a for a in range(-self.v_max,self.v_max,resolution)])

    def get_p(self,current_state, action, next_state):
        ##TODO add the prob determination via knn here
        pass

    def get_r(self,current_state, action, next_state):
        return self.R[current_state][action][next_state]
    
    def action_space_discretization(self):
        pass

    def phi(self,y) -> int :
        return self.hill_size*np.sin((2*np.pi*y)/self.y_max)
    
    def sim_input(self, t):
        return 1

    def update_state(self):
        #TODO add  check to see if valid (?)
        self.state = (self.position,self.velocity)

    def calculate_reward_set(self, S, A):
        ##TODO define reward function for numberline
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

    def calculate_observation_set(self,S) :
        O = {}
        for state in S:
            o =  self.h(state[0],state[1])
            O[state] = o
        return O

    def h(self,position=None,velocity=None) -> int:
        #observation of the velocity
        if position ==None:
            position=self.position
        if velocity == None:
            velocity =self.velocity
        retval =  int(position + self._noise_sensor(velocity))
        #check for bounds
        retval =self._check_bounds(retval,self.y_max)
        return retval

    def _check_bounds(self,retval,max_val):
        if retval > max_val:
            retval =max_val
        elif retval < -max_val:
            retval= -max_val
        return retval

    def _next_position(self,state):
        retval = state[0] + state[1]*1 #time step one unit (u+vt)
        return self._check_bounds(retval,self.y_max)
    
    def calculate_transition_prob_set(self,S, A):
        transition_mat = {}
        for state in S: #current State
            has_crashed = random.uniform(0, 1) < ((np.abs(state[1])) * self.p_c)/self.v_max
            a_dict ={}
            for action in A:  #current action
                s_dict = {}
                
                if has_crashed:
                    next_velocity = 0
                else:
                    next_velocity = state[1] + (1 / self.m) * self._net_force(action) + self._noise_dynamics(state[1])
                next_velocity =self._check_bounds(next_velocity,self.v_max)
                next_position = self._next_position(state)
                next_state= (next_position,next_velocity)
                s_dict[next_state] = 1 #transition probability 1 for now
                # calculate prob here, from the output of the sys dynamincs equation using it with the probability bins (another function) to calculate p, using knn
            
                a_dict[action] = s_dict
            transition_mat[tuple(state)] = a_dict
        return transition_mat
                
    def _probability_of_state(self):
        pass
    
    def _knn(self):
        pass

    def possible_actions(self, present_state):
        ##TODO fit to numberline problem
        return self.A
    

    def _net_force(self, input_force) -> int:
        f_net = int(input_force + derivative(self.phi, self.state[0]) )
        return f_net
    
    def _noise_sensor(self,v):
        return np.random.normal(0, np.abs(0.5*v))
    
    def _noise_dynamics(self,v):
        #TODO change to new speed wobble 
        return np.random.normal(0, np.abs(0.1*v))
        
   