import numpy as np
import time
from environment import YahtzeeEnvironment
from simulator import Simulator
from mdp import MDP


Pe = 0
initial_state = (1,1,3,4,4)
yahtzee_env = YahtzeeEnvironment(Pe)
print('env built')
yahtzee_mdp = MDP(yahtzee_env)
print('mdp made')
yahtzee_pol = yahtzee_mdp.value_iteration(0.01, 1)
print('value iteration done')
yahtzee_sim = Simulator(yahtzee_env, initial_state)
yahtzee_env.visualize([yahtzee_sim.state], yahtzee_pol)

while not yahtzee_sim.exitProgram:
    yahtzee_sim.nextStepPolicy(yahtzee_pol)
    yahtzee_env.visualize([yahtzee_sim.state], yahtzee_pol)
    time.sleep(0.5)