import numpy as np
from pynput import keyboard
import time

from configuration import Environment

class GridworldSimulator:
    def __init__(self, environment, initial_state):
        self.exitProgram = 0

        self.environment = environment
        self.grid = self.environment.grid
        self.state = initial_state

    def run(self):
        # keyboard listener
        listener = keyboard.Listener(on_press=self.takeAction)
        listener.start()

        self.drawGridworld()
        while not self.exitProgram:
            time.sleep(0.2)
    
    def moveToNextState(self, action):
        actions = self.environment.P[tuple(self.state)]

        transition = actions[action]
        states = list(transition.keys())
        next_state_idx = np.random.choice(np.arange(len(states)), p=list(transition.values()))
        next_state = states[next_state_idx]
        print(f'Next state: {next_state}, Probability of reaching this state: {transition[next_state]}')
        self.state = next_state
        print(f'Output: {self.environment.O[tuple(self.state)]}')
        self.drawGridworld()

    def drawGridworld(self, wall_char='X', state_char='O'):
        for i in range(len(self.grid)):
            row = '|'
            for j in range(len(self.grid[0])):
                if i == self.state[0] and j == self.state[1]:
                    row += f'{state_char}|'
                    continue

                if self.grid[i, j] == '0':
                    row += '_|'
                elif self.grid[i, j] == '1':
                    row += f'{wall_char}|'
                else:
                    row += f'{self.grid[i, j]}|'
            print(row)

        print('\n\n\n')

    def takeAction(self, key):
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
        elif key.char == 'q':
            self.exitProgram = 1
            return
        else:
            print(f'Invalid key pressed: {key}')
            return
        
        print(f'Action: {action}')
        self.moveToNextState(action)