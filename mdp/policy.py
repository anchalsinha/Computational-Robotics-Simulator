import numpy as np
from abc import ABC, abstractmethod

class MDP(ABC):
    def __init__(self, environment, R):
        self.environment = environment
        self.R = R
        self.exitProgram = 0

    # Doesn't work when gamma = 1.0
    def value_iteration(self, termination_epsilon = 0.01, gamma = 0.5):
        policy, value, value_delta = {}, {}, 1
        while value_delta > termination_epsilon:
            value_delta = 0
            for state in self.environment.S:
                best_action, best_value = None, None
                for action in self.environment.A:
                    action_value = 0
                    for next_state in self.environment.S:
                        movement_prob = self.environment.P.get(state, {}).get(action, {}).get(next_state, 0)
                        movement_reward = self.R(state, action, next_state)
                        action_value += movement_prob * (movement_reward + gamma * value.get(next_state, 0))
                    
                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                value_delta = max(value_delta, abs(value.get(state, 0) - best_value))
                policy[state], value[state] = best_action, best_value
        return policy
        
    def policy_iteration(self, termination_epsilon = 0.01, gamma = 0.5):
        policy, value, value_delta  = {}, {}, 1

        # Randomly initialize policy
        for state in self.environment.S:
            policy[state] = self.environment.A[np.random.choice(range(len(self.environment.A)), 1)[0]]

        while True:
            # Policy Evaluation
            while value_delta > termination_epsilon:
                value_delta = 0
                for state in self.environment.S:
                    state_value = 0
                    for next_state in self.environment.S:
                        movement_prob = self.environment.P.get(state, {}).get(policy[state], {}).get(next_state, 0)
                        movement_reward = self.R(state, policy[state], next_state)
                        state_value += movement_prob * (movement_reward + gamma * value.get(next_state, 0))

                    value_delta = max(value_delta, abs(value.get(state, 0) - state_value))
                    value[state] = state_value

            # Policy Improvement
            is_policy_stable = True 
            for state in self.environment.S:
                best_action, best_value = None, None
                for action in self.environment.A:
                    action_value = 0
                    for next_state in self.environment.S:
                        movement_prob = self.environment.P.get(state, {}).get(action, {}).get(next_state, 0)
                        movement_reward = self.R(state, action, next_state)
                        action_value += movement_prob * (movement_reward + gamma * value.get(next_state, 0))

                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                # Need to fix bug that occurs if two policies have equally good values and the algorithm switches between the two
                # TODO: Is it possible that two policies have equal overall values but different values at different states
                if policy[state] != best_action and value[state] != best_value:
                    is_policy_stable = False

                policy[state] = best_action

            if is_policy_stable:
                break
        return policy
