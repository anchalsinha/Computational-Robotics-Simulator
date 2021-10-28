import numpy as np

from environment import NumberLineEnvironment
from simulator import Simulator


initial_state =  (0,0)
numberline_environment = NumberLineEnvironment()
numberline_simulator = Simulator(numberline_environment)
numberline_simulator.run()