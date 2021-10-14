import numpy as np
import time
from pynput import keyboard

class Simulator:
    def __init__(self, environment, initial_state):
        self.environment = environment
        self.state = initial_state

        self.exitProgram = 0
    
    def nextStep(self, action):
        '''
        Given the selected action, randomly choose the next state and output based on the transition
        probabilities and change the current state
        '''
        actions = self.environment.P[tuple(self.state)]

        transition = actions[action]
        states = list(transition.keys())
        next_state_idx = np.random.choice(np.arange(len(states)), p=list(transition.values()))
        next_state = states[next_state_idx]
        print(f'Next state: {next_state}, Probability of reaching this state: {transition[next_state]}')
        self.state = next_state

        outputs = self.environment.O[tuple(self.state)]
        output = np.random.choice(outputs[:,0], p=outputs[:,1])
        print(f'Output: {output}')

    def nextStepPolicy(self, policy):
        return self.nextStep(policy[self.state])
 
    def run_policy(self, policy):
        '''
        Simulation loop with MDP policy
        '''
        pass
