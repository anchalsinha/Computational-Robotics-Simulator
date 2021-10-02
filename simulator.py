import numpy as np
import matplotlib.pyplot as plt
from pynput import keyboard
import time
import sys

from configuration import S, A, P, O

quitKey = 0

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

def moveToNextState(action):
    global state
    actions = P[tuple(state)]

    transition = actions[action]
    states = list(transition.keys())
    next_state_idx = np.random.choice(np.arange(len(states)), p=list(transition.values()))
    next_state = states[next_state_idx]
    print(f'Next state: {next_state}, Probability of reaching this state: {transition[next_state]}')
    state = next_state
    # print(f'Output: {O[tuple(state)]}')
    drawGridworld()

def drawGridworld(wall_char='X', state_char='O'):
    for i in range(len(grid)):
        row = '|'
        for j in range(len(grid[0])):
            if i == state[0] and j == state[1]:
                row += f'{state_char}|'
                continue

            if grid[i, j] == '0':
                row += '_|'
            elif grid[i, j] == '1':
                row += f'{wall_char}|'
            else:
                row += f'{grid[i, j]}|'
        print(row)

    print('\n\n\n')

def takeAction(key):
    global quitKey

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
        quitKey = 1
        return
    else:
        print(f'Invalid key pressed: {key}')
        return
    
    print(f'Action: {action}')
    moveToNextState(action)

listener = keyboard.Listener(on_press=takeAction)
listener.start()

if __name__ == '__main__':
    drawGridworld()
    while not quitKey:
        time.sleep(1)