from abc import ABC, abstractmethod

class Environment(ABC):
    def __init__(self, S, A, P, O, R):
        self.S, self.A, self.P, self.O, self.R = S, A, P, O, R
    
    @abstractmethod
    def calculate_phi(self, state):
        pass

    @abstractmethod
    def calculate_reward(self, state):
        pass

    @abstractmethod
    def calculate_observation(self, state):
        pass

    @abstractmethod
    def calculate_transition_prob(self, state, action):
        pass

    @abstractmethod
    def visualize(self, states):
        pass
    