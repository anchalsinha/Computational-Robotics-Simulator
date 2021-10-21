import numpy as np
import time
from abc import ABC, abstractmethod
from pynput import keyboard
from .base_simulator import Simulator

class NumberlineSimulator(Simulator):
    # TODO: Implement this function
    def visualize(self):
        nline = self.environment.position_space
        for i in range(len(nline)):
            if i == self.state[0]:
                print("O")
            else:
                print("-")
            
        print('\t')

    def keyboardCallback(self, key):
        '''
        Keyboard listener function to select an action based on key input
        '''
        A = self.environment.A

        try:
            if key == keyboard.Key.left:
                action = A[0]
            elif key == keyboard.Key.right:
                action = A[1]
            elif key == keyboard.Key.up:
                action = A[2]
            elif key.char == 'q':
                self.exitProgram = 1
                return
            self.nextStep(action)
        except:
            pass
    
    def run(self):
        # keyboard listener in background thread
        listener = keyboard.Listener(on_press=self.keyboardCallback)
        listener.start()

        self.visualize()
        while not self.exitProgram:
            time.sleep(0.1)
    
    
    def run_policy(self, policy):
        # keyboard listener in background thread
        listener = keyboard.Listener(on_press=self.keyboardCallback)
        listener.start()

        while not self.exitProgram:
            self.nextStep(policy[self.state])
            self.visualize()
            time.sleep(0.5)