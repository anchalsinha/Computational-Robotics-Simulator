import numpy as np

from environment import NumberLineEnvironment
from simulator import NumberlineSimulator
initial_state =  (0,0)
numberline_environment = NumberLineEnvironment()
numberline_simulator = NumberlineSimulator(numberline_environment,initial_state)
numberline_simulator.run()