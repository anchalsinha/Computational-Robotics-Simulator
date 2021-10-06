from .base_environment import Environment
import numpy as np
from collections import defaultdict
from abc import ABC, abstractmethod


class MDP(ABC):
    def __init__(self, environment):
        self.environment = environment

        self.exitProgram = 0


    def value_iteration(self, termination_epsilon = 0.01):
        policy, value, value_delta, termination_epsilon = {}, {}, 0
        while value_delta > termination_epsilon:
            value_delta = 0
            for state in self.state:
                best_action, best_value = None, None
                for action in self.action:
                    action_value = 0
                    for next_state in self.state:
                        movement_prob = self.p(state, action, next_state)
                        movement_reward = self.r(state, action, next_state)
                        action_value += movement_prob * (movement_reward + self.gamma * value[next_state])
                    
                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                value_delta = max(value_delta, abs(value[state] - best_value))
                policy[state], value[state] = best_action, best_value
                
    def policy_iteration(self, termination_epsilon = 0.01):
        policy, value, value_delta  = {}, {}, 0

        # Randomly initialize policy
        for state in self.state:
            policy[state] = np.random.choice(self.action)

        while True:
            # Policy Evaluation
            while value_delta > termination_epsilon:
                value_delta = 0
                for state in self.state:
                    state_value = 0
                    for next_state in self.state:
                        movement_prob = self.p(state, policy[state], next_state)
                        movement_reward = self.r(state, policy[state], next_state)
                        state_value += movement_prob * (movement_reward + self.gamma * value[next_state])

                    value_delta = max(value_delta, abs(value[state] - state_value))
                    value[state] = state_value

            # Policy Improvement
            is_policy_stable = True 
            for state in self.state:
                best_action, best_value = None, None
                for action in self.action:
                    action_value = 0
                    for next_state in self.state:
                        movement_prob = self.p(state, action, next_state)
                        movement_reward = self.r(state, action, next_state)
                        action_value += movement_prob * (movement_reward + self.gamma * value[next_state])

                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                # Need to fix bug that occurs if two policies have equally good values and the algorithm switches between the two
                # TODO: Is it possible that two policies have equal overall values but different values at different states
                if policy[state] != best_action and value[state] != best_value:
                    is_policy_stable = False

                policy[state] = best_action

            if is_policy_stable:
                break
                
