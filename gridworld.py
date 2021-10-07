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

# TODO: Find a better place to define this
R = {}
for state in gridworld_environment.S:
    for action in gridworld_environment.A:
        for next_state in gridworld_environment.S:
            R.setdefault(state, {})
            R[state].setdefault(action, {})
            R[state][action][next_state] = 1 if grid[next_state] == 'D' or grid[next_state] == 'H' else 0

gridworld_mdp = MDP(gridworld_environment, R)
gridworld_policy = gridworld_mdp.value_iteration(0.01, 0.5)
# gridworld_policy = gridworld_mdp.policy_iteration(0.01, 0.5)

gridworld_simulator = GridworldSimulator(gridworld_environment, initial_state)
gridworld_simulator.run_policy(gridworld_policy)