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

        self.visualize()

    @abstractmethod
    def visualize(self):
        pass

    @abstractmethod 
    def run(self):
        pass


class GridworldSimulator(Simulator):
    def visualize(self):
        '''
        Draws the current gridworld state in the command window
        '''
        grid = self.environment.grid
        for i in range(len(grid)):
            row = '|'
            for j in range(len(grid[0])):
                if (i, j) == self.state:
                    row += 'O|'
                elif grid[i, j] == '0':
                    row += '_|'
                elif grid[i, j] == '1':
                    row += 'X|'
                else:
                    row += f'{grid[i, j]}|'
            print(row)

        print('\n\n\n')

    def keyboardCallback(self, key):
        '''
        Keyboard listener function to select an action based on key input
        '''
        A = self.environment.A
        if key == keyboard.Key.left:
            action = A[0]
        elif key == keyboard.Key.right:
            action = A[1]
        elif key == keyboard.Key.up:
            action = A[2]
        elif key == keyboard.Key.down:
            action = A[3]
        elif key == keyboard.Key.space:
            action = A[4]
        elif 'char' in key and key.char == 'q':
            self.exitProgram = 1
            return
        else:
            print(f'Invalid key pressed: {key}')
            return
        
        self.nextStep(action)

    def run(self):
        # keyboard listener in background thread
        listener = keyboard.Listener(on_press=self.keyboardCallback)
        listener.start()

        self.visualize()
        while not self.exitProgram:
            time.sleep(0.1)