from abc import ABC, abstractmethod

class Environment(ABC):
    def __init__(self, S, A, P, O, R, functions):
        self.S, self.A, self.P, self.O, self.R = S, A, P, O, R
        self.basis_functions = functions
    
    @abstractmethod
    def calculate_phi(self, state):
        pass
    
    @abstractmethod
    def visualize(self, states):
        pass
    