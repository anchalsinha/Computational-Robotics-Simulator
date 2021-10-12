import numpy as np
from environment import YahtzeeEnvironment
from simulator import YahtzeeSimulator
from mdp import MDP



initial_state = (1,1,3,4,4)
yahtzee_env = YahtzeeEnvironment(0)
yahtzee_mdp = MDP(yahtzee_env)
yahtzee_pol = yahtzee_mdp.value_iteration(0.01, 1)
yahtzee_sim = YahtzeeSimulator(yahtzee_env, initial_state)