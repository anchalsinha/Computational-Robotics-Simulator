import numpy as np

from environment import NumberLineEnvironment
from simulator import NumberlineSimulator
from mdp.policy import MDP

running_what = 'rrt' #TODO add as argument 
numberline_environment = NumberLineEnvironment(running_what)
ymax=numberline_environment.y_max
vmax= numberline_environment.v_max
initial_state =  (ymax,0.0)

numberline_simulator = NumberlineSimulator(numberline_environment,initial_state)

# path = numberline_environment.rrt((-10, 4), (0, 0))
# print(path)

#MDP
if running_what == 'mdp':
    numberline_mdp = MDP(numberline_environment)
    numberline_policy = numberline_mdp.value_iteration(0.01)
    numberline_simulator.run_policy(numberline_policy)

elif running_what == 'rrt':
    numberline_simulator.run_randompaths()