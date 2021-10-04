import numpy as np

from configuration import Environment
from simulator import GridworldSimulator

grid = np.array([
        [0, 0, 0, 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 'D', 0, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 'S', 0, 1],
])
Pe = 0.3
initial_state = [0, 2]

environment = Environment(grid, Pe)
simulator = GridworldSimulator(environment, initial_state)
simulator.run()