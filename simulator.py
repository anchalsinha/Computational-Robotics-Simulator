import numpy as np
import matplotlib.pyplot as plt
from pynput import keyboard
import time
import sys

from configuration import S, A, P, O

# define grid
grid = np.array([
        [0, 0, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 'D', 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 'S', 0, 1],
])
Rd_loc = list(zip(*np.where(grid == 'D')))[0]
Rs_loc = list(zip(*np.where(grid == 'S')))[0]

state = [0, 2]

def moveToNextState():
    actions_dict = P[state]
    actions = actions_dict.keys()
    for action in actions:
        transition = actions[action]
        next_state = np.random.choice(transition.keys(), p=transition.values())
        print(f'Next state: {next_state}, Probability of reaching this state: {transition[next_state]}')
    


def takeAction(key):
    if key == keyboard.Key.left:
        action = A[0]
    elif key == keyboard.Key.right:
        action = A[1]
    elif key == keyboard.Key.down:
        action = A[2]
    elif key == keyboard.Key.up:
        action = A[3]
    elif key == keyboard.Key.space:
        action = A[4]
    elif key == keyboard.Key.q:
        sys.exit(0)
    else:
        print('Invalid key pressed')
        return

    
    print(f'Action: {action}')

listener = keyboard.Listener(on_press=takeAction)
listener.start()



if __name__ == '__main__':
    while True:
        time.sleep(1)