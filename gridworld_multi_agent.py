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
initial_states = [(0, 2), (0, 0), (4, 0)] # initial states assuming that this state lies in an empty cell on the grid


gridworld_environment = GridworldEnvironment(grid, Pe)

gridworld_mdp = MDP(gridworld_environment)
gridworld_policy = gridworld_mdp.value_iteration_FA(0.01, 0.5)
# gridworld_policy = gridworld_mdp.policy_iteration(0.01, 0.5)

simulators = [Simulator(gridworld_environment, state) for state in initial_states]
gridworld_environment.visualize([s.state for s in simulators], gridworld_policy)

while True:
    for sim in simulators:
        sim.nextStepPolicy(gridworld_policy)
    gridworld_environment.visualize([s.state for s in simulators], gridworld_policy)
    time.sleep(0.5)