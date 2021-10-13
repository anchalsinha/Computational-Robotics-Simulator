import numpy as np
import time
from abc import ABC, abstractmethod
from pynput import keyboard

class Simulator(ABC):
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
 
    def run_policy(self, policy):
        '''
        Simulation loop with MDP policy
        '''
        while not self.exitProgram:
            self.nextStep(policy[self.state])
            print("Policy: ")
            for i in range(len(self.environment.grid)):
                row = '|'
                for j in range(len(self.environment.grid[0])):
                    if policy[i, j] == (0, 0):
                        row += 'S|'
                    elif policy[i, j] == (1, 0):
                        row += '↑|'
                    elif policy[i, j] == (-1, 0):
                        row += '↓|'
                    elif policy[i, j] == (0, 1):
                        row += '→|'
                    else:
                        row += f'←|'
                print(row)

            print("Reward: ")
            for i in range(len(self.environment.grid)):
                row = '|'
                for j in range(len(self.environment.grid[0])):
                    row += f'{self.environment.R[(0,0)][(0,0)][i, j]}|'
                print(row)

            self.visualize()
            time.sleep(0.5)

    @abstractmethod
    def visualize(self):
        pass