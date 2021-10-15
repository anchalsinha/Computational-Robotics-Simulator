import numpy as np

from environment import NumberLineEnvironment
from simulator import NumberlineSimulator
from mdp.policy import MDP


initial_state =  (0,0)
numberline_environment = NumberLineEnvironment()
numberline_simulator = NumberlineSimulator(numberline_environment,initial_state)

numberline_mdp = MDP(numberline_environment)
numberline_policy = numberline_mdp.value_iteration(0.01)

numberline_simulator.run_policy(numberline_policy)