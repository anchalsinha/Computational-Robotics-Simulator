import numpy as np

from environment import NumberLineEnvironment
from simulator import Simulator

numberline_environment = NumberLineEnvironment()
numberline_simulator = Simulator(numberline_environment)
numberline_simulator.run()