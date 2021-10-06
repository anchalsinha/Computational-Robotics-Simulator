import numpy as np

from environment import NumberLineEnvironment
from simulator import NumberlineSimulator

numberline_environment = NumberLineEnvironment()
numberline_simulator = NumberlineSimulator(numberline_environment)
numberline_simulator.run()