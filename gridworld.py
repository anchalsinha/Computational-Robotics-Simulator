import numpy as np
import time

from environment import GridworldEnvironment
from simulator import Simulator
from mdp import MDP

# 0 - empty
# 1 - wall
# characters (i.e. 'D' and 'S') - target
# TODO: different indication of road which will have negative reward
grid = np.array([
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 'D', 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 'S', 0, 1],
])
Pe = 0.3 # error probability
initial_state = (0, 2) # initial state assuming that this state lies in an empty cell on the grid


gridworld_environment = GridworldEnvironment(grid, Pe)

gridworld_mdp = MDP(gridworld_environment)
gridworld_policy = gridworld_mdp.value_iteration(0.01, 0.5)
# gridworld_policy = gridworld_mdp.policy_iteration(0.01, 0.5)

gridworld_simulator = Simulator(gridworld_environment, initial_state)
gridworld_environment.visualize([gridworld_simulator.state])

while not gridworld_simulator.exitProgram:
    gridworld_simulator.nextStepPolicy(gridworld_policy)
    gridworld_environment.visualize([gridworld_simulator.state])
    time.sleep(0.5)