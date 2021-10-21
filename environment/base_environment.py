from abc import ABC, abstractmethod

class Environment(ABC):
    def __init__(self, S, A, P, O, R):
        self.S, self.A, self.P, self.O, self.R = S, A, P, O, R

    '''
    Visualize evolution of MDP solution
    '''
    @abstractmethod
    def visualize(self, states):
        pass
        