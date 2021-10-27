import numpy as np

from environment import NumberLineEnvironment
from simulator import NumberlineSimulator
from mdp.policy import MDP


numberline_environment = NumberLineEnvironment()
ymax=numberline_environment.y_max
vmax= numberline_environment.v_max
initial_state =  (ymax,0.0)

numberline_simulator = NumberlineSimulator(numberline_environment,initial_state)

# path = numberline_environment.rrt((-10, 4), (0, 0))
# print(path)

numberline_mdp = MDP(numberline_environment)
numberline_policy = numberline_mdp.value_iteration(0.01)

numberline_simulator.run_policy(numberline_policy)