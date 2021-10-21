import numpy as np
import random
from scipy.misc import derivative
import pdb

from .base_environment import Environment

class NumberLineEnvironment(Environment):
    def __init__(self,gamma = 0.8,hill_size=2,resolution=0.1,target_state= (0,0)):
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

        #prm
        self.prm_time_upper_bound = 2
        


        self.position = 0  # position
        self.velocity = 0  # velocity
        self.time = 0

        self.target_state = target_state


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
        position_resolution = int(2.0*self.y_max/resolution)
        velocity_resolution = int(2.0*self.v_max/resolution)
        self.position_space = np.array([a for a in range(-self.y_max,self.y_max,position_resolution)])
        self.velocity_space = np.array([a for a in range(-self.v_max,self.v_max,velocity_resolution)])

    def get_p(self,current_state, action, next_state):
        ##TODO add the prob determination via knn here
        pass

    def get_r(self,current_state, action, next_state):
        return self.R[current_state][action][next_state]

    def action_space_discretization(self):
        pass

    def phi(self,y) -> int :
        """potential field"""
        return self.hill_size*np.sin((2*np.pi*y)/self.y_max)

    def sim_input(self, t):
        return 1

    def update_state(self):
        #TODO add  check to see if valid (?)
        self.state = (self.position,self.velocity)

    def calculate_reward_set(self, S, A):
        """
        Iterating through all the states in the state space
        ### Rewards
        - 1 for next state desired state
        - v-1 for next state undesired state
        """

        R = {}
        for state in S:
            for action in A:
                for next_state in S:
                    R.setdefault(state, {})
                    R[state].setdefault(action, {})
                    if next_state == self.target_state:
                        R[state][action][next_state] = 1
                    elif next_state != self.target_state:
                        R[state][action][next_state] = -1

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

    def _next_velocity(self,state,action):
        """
        Velocity of next state \\
            - Influence of net force 
            - Influence of noise due to system dynamics
            - Checks bounds
        """
        next_velocity = state[1] + (1 / self.m) * self._net_force(action) + self._noise_dynamics(state[1])
        return self._check_bounds(next_velocity,self.v_max)

    def _next_state(self, state, action):
        has_crashed = random.uniform(0, 1) < ((np.abs(state[1])) * self.p_c)/self.v_max
        if has_crashed:
            next_velocity = 0.0
        else:
            next_velocity = self._next_velocity(state, action)
        next_position = self._next_position(state)
        next_state = (next_posiiton, next_velocity)
        return next_state


    def calculate_transition_prob_set(self,S, A):
        transition_mat = {}
        for state in S: #current State
            a_dict = {}
            for action in A:  #current action
                s_dict = {}
                has_crashed = random.uniform(0, 1) < ((np.abs(state[1])) * self.p_c)/self.v_max
                if has_crashed:
                    next_velocity = 0
                else:
                    next_velocity = self._next_velocity(state, action)
                next_position = self._next_position(state)
                next_state = (next_position,next_velocity)
                s_dict[next_state] = 1 #transition probability 1 for now
                # calculate prob here, from the output of the sys dynamincs equation using it with the probability bins (another function) to calculate p, using knn

                a_dict[action] = s_dict
            transition_mat[tuple(state)] = a_dict
        return transition_mat

    def calculate_discrete_transition_probability_set(self, S, A):
        samples = 100
        discrete_transition_dict = {}
        # Initialize the probability set with zero
        for state in S:
            for action in A:
                for new_state in S:
                    dicreter_transition_dict[(state,action,new_state)] = 0.0

        for state in S:
            for action in A:
                possiblity_next_states = {}
                for i in range(samples):
                    # iterate the system dynamics 100 times form (S(i),A(i))
                    next_state = next_state(state, action)
                    if next_state in possible_next_states:
                        possible_next_states[next_state] = possible_next_states[next_state] + 1
                    else:
                        possible_next_states[next_state] = 1
                # Populate the transition dictionary
                for a_next_state in possible_next_states:
                    normalized_prob = possible_next_states[a_next_state]/samples*100.0
                    discrete_transition_dict[(state,action,a_next_state)] = normalized_prob
        return discrete_transition_dict

    def _probability_of_state(self):
        pass

    def _knn(self):
        pass

    def possible_actions(self, present_state):
        ##TODO fit to numberline problem
        return self.A


    def _net_force(self, input_force) -> int:
        """The net force \\
           Input force + force exerted by loc in the potential field
        """
        f_net = int(input_force + derivative(self.phi, self.state[0]) )
        return f_net

    def _noise_sensor(self,v):
        return np.random.normal(0, np.abs(0.5*v))

    def _noise_dynamics(self,v):
        """
        Speed wobble dynamics
        """
        #TODO change to new speed wobble
        return np.random.normal(0, np.abs(0.1*v))

    def possible_actions(self,a):
        return self.A
    
    def possible_jumps(self,actions,state):
        return self.S

    # Overload
    def possible_actions(self, state):
        return self.A

    ## PRM ###############
    ##---------------------------------------------------------
    # Two points in state space can be connected if there exists a constant input fi that drives the initial state to the final state (over some upper-bounded duration of time)

    def PRM(self):
        pass

    def _motion_edge(self,current_state,next_state,action):
        """
        Two points in state space can be connected if there exists a constant input fi that drives the initial state to the final state (over some upper-bounded duration of time)

        Input = f_net

        Return:
            True if transition exists \\
            False is not

        """
        for action in range(-1,1):
            next_position = self._next_position(current_state)
            next_velocity = self._next_velocity(current_state,action)
        




   
