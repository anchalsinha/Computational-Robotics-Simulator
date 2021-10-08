import numpy as np
import random
from scipy.misc import derivative

from .base_environment import Environment

class NumberLineEnvironment(Environment):
    def __init__(self):
        # TODO: Define S, A, P, and O
        # Environment.__init__(self, S, A, P, O)
        self.v_max = 10
        self.y_max = 10
        self.p_c = 5
        self.m = 10
        self.hill_size = 2 #TODO make input

        self.position = 0  # position
        self.velocity = 0  # velocity
        self.time = 0
        
        self.position_list = []
        self.velocity_list = []
        self.observation_list = []

        self.position_space = np.array([a for a in range(-self.y_max,self.y_max,1)])
        self.velocity_space = np.array([a for a in range(-self.v_max,self.v_max,1)])
        self.update_state()
        # define state and action spaces
        S = (self.position,self.velocity)
        A = [-1,0,1]

        O = self.calculate_observation_set()
        P = self.calculate_transition_prob_set(S, A)

        Environment.__init__(self, S, A, P, O)
        
    def phi(self,y):
        return self.hill_size*np.sin((2*np.pi*y)/self.y_max)
    
    def sim_input(self, t):
        return 1

    def update_state(self):
        #TODO add  check to see if valid (?)
        self.state = (self.position,self.velocity)
        self.S = (self.position,self.velocity)
    
    def calculate_observation_set(self):
        return self.position + self._noise_sensor(self.velocity)
    
    def calculate_transition_prob_set(self,S, A):
        for state in S: #current State
            has_crashed = random.uniform(0, 1) < ((np.abs(self.state[1]) - self.v_max) * self.p_c)/self.v_max
            
            for a in A:
                if has_crashed:
                    self.velocity = 0
                else:
                    self.velocity = self.state[1] + (1 / self.m) * self._net_force(sys_input) + self._noise_dynamics(self.state[1])
                for next_state in S:
                    pass


    def f(self,sys_input,dt):
        # from @alexswerdlow
        # update state
        self.position = self.velocity * dt
        has_crashed = random.uniform(0, 1) < ((np.abs(self.state[1]) - self.v_max) * self.p_c)/self.v_max
        if has_crashed:
            self.velocity = 0
        else:
            self.velocity = self.state[1] + (1 / self.m) * self._net_force(sys_input) + self._noise_dynamics(self.state[1])
        
        self.update_state()
    
    def _net_force(self, input_force):
        f_net = input_force + derivative(self.phi, self.state[0]) 
        return f_net
    
    def _noise_sensor(self,v):
        return np.random.normal(0, 0.5*v)
    
    def _noise_dynamics(self,v):
        #TODO change to new speed wobble 
        return np.random.normal(0, 0.1*v)
        
    def update_variables_to_plot(self):
        #OLD
        self.position_list.append(self.state[0])
        self.velocity_list.append(self.state[1])
        self.observation_list.append(self.h())
        self.update_state()
    
    def vars_to_plot(self):
        #OLD
        return [self.position_list,self.velocity_list,self.observation_list]
    
    def cleanup_variable_store(self):
        #OLD
        self.position_list = []
        self.velocity_list = []
        self.observation_list = []

