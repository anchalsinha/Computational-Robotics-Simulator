import numpy as np
import time
from abc import ABC, abstractmethod
from pynput import keyboard

from .base_simulator import Simulator

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
        '''
        Simulation loop
        '''
        # keyboard listener in background thread
        listener = keyboard.Listener(on_press=self.keyboardCallback)
        listener.start()

        self.visualize()
        while not self.exitProgram:
            time.sleep(0.1)