import numpy as np
import time

from pynput import keyboard

from environment import GridworldEnvironment
from simulator import Simulator
from mdp import MDP

def keyboardCallback(key):
    '''
    Keyboard listener function to select an action based on key input
    '''
    A = gridworld_environment.A
    try:
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
            gridworld_simulator.exitProgram = 1
            return
        gridworld_simulator.nextStep(action)
        gridworld_environment.visualize([gridworld_simulator.state])
    except:
        pass

listener = keyboard.Listener(on_press=keyboardCallback)
listener.start()


# Grid Input:
# 0 - empty
# 1 - wall
# 'D' and 'S' - targets
# 'W' - road
grid = np.array([
    [0, 0, 0, 0, 'W'],
    [0, 1, 1, 0, 'W'],
    [0, 0, 'D', 0, 'W'],
    [0, 1, 1, 0, 'W'],
    [0, 0, 'S', 0, 'W'],
])
Pe = 0.3 # error probability
initial_state = (0, 2) # initial state assuming that this state lies in an empty cell on the grid

# Run simulator
gridworld_environment = GridworldEnvironment(grid, Pe)
gridworld_simulator = Simulator(gridworld_environment, initial_state)
gridworld_environment.visualize([gridworld_simulator.state])

while not gridworld_simulator.exitProgram:
    time.sleep(0.5)