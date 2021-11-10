import numpy as np
from collections import defaultdict
from environment import GridworldEnvironment
from simulator import Simulator
import random

if __name__ == "__main__":

    grid = np.array([
    [0, 0, 0, 0, 2],
    [0, 0, 0, 0, 2],
    [0, 1, 'D', 1, 2],
    [0, 0, 0, 0, 2],
    [0, 0, 'S', 0, 2],
    ])

    Pe = 0.2 # error probability
    initial_state = (1, 1) # initial state assuming that this state lies in an empty cell on the grid


    gridworld_environment = GridworldEnvironment(grid, Pe)
    sim = Simulator(gridworld_environment, initial_state)

    initial_belief = defaultdict(int)
    initial_belief[initial_state] = 1

    curr_bel = initial_belief
    curr_data = "action"
    num_iters = 10
    for i in range(num_iters):

        if curr_data == "action":
            action = random.choice(gridworld_environment.A)
            curr_bel = gridworld_environment.bayes_filter(curr_bel, action, curr_data)

            sim.nextStep(action)
            curr_data = "observation"
        else:
            curr_state = sim.state
            obs = gridworld_environment.get_o(curr_state)

            curr_bel = gridworld_environment.bayes_filter(curr_bel, obs, curr_data)
            curr_data = "action"

        for k,v in curr_bel.items():
            print("%s: %s" % (k,v))
        print(sum(curr_bel.values()))
        print()