from os import stat
import numpy as np
import time
from abc import ABC, abstractmethod
from pynput import keyboard
import matplotlib.pyplot as plt

import environment
from .base_simulator import Simulator

class NumberlineSimulator(Simulator):

    def __init__(self, environment, initial_state):
        super().__init__(environment, initial_state)
        self.state = initial_state

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
    
    def run_randompaths(self):
        rrt_traj = self.environment.rrt()
        self.viz_rrt(rrt_traj)
    
    def viz_rrt(self,rrt_traj):
        y_max = self.environment.y_max
        v_max = self.environment.v_max
        plt.xlim(-y_max,y_max)
        plt.ylim(-v_max,v_max)
        plt.plot(rrt_traj)
        plt.show()

       
            
    
    def run_policy(self, policy):
        # keyboard listener in background thread
        listener = keyboard.Listener(on_press=self.keyboardCallback)
        listener.start()
        # print(policy)
        while not self.exitProgram:
            self.nextStep(policy[self.state])
            self.visualize()
            time.sleep(0.5)