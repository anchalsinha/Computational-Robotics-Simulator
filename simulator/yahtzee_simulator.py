import numpy as np
from .base_simulator import Simulator

class YahtzeeSimulator(Simulator):
    def visualize(self):
        print(self.state)