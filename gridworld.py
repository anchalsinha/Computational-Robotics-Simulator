import numpy as np

from environment import GridworldEnvironment
from simulator import GridworldSimulator
from mdp import MDP

grid = np.array([
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 'D', 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 'S', 0, 1],
])
Pe = 0.3
initial_state = (0, 2)

gridworld_environment = GridworldEnvironment(grid, Pe)

def reward(state, action, next_state):
    if next_state == (2, 2) or next_state == (4, 2):
        return 1
    else:
        return 0

R = np.zeros(grid.shape)
R[np.argwhere(grid == 'D')] = 1
R[np.argwhere(grid == 'S')] = 1

gridworld_mdp = MDP(gridworld_environment, reward)
#gridworld_policy = gridworld_mdp.value_iteration(0.01, 0.5)
gridworld_policy = gridworld_mdp.policy_iteration(0.01, 0.5)

gridworld_simulator = GridworldSimulator(gridworld_environment, initial_state)
gridworld_simulator.run_policy(gridworld_policy)