import numpy as np

from environment import GridworldEnvironment
from simulator import GridworldSimulator
from mdp import MDP

# 0 - empty
# 1 - wall
# 2 - road
# characters (i.e. 'D' and 'S') - target
# TODO: different indication of road which will have negative reward
grid = np.array([
    [0, 0, 0, 0, 2],
    [0, 1, 1, 0, 2],
    [0, 0, 'D', 0, 2],
    [0, 1, 1, 0, 2],
    [0, 0, 'S', 0, 2],
])
Pe = 0.3 # error probability
initial_state = (0, 2) # initial state assuming that this state lies in an empty cell on the grid


gridworld_environment = GridworldEnvironment(grid, Pe)

gridworld_mdp = MDP(gridworld_environment)
gridworld_policy = gridworld_mdp.value_iteration(0.01, 0.5)
# gridworld_policy = gridworld_mdp.policy_iteration(0.01, 0.5)

gridworld_simulator = GridworldSimulator(gridworld_environment, initial_state)
gridworld_simulator.run_policy(gridworld_policy)