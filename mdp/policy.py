import numpy as np
from abc import ABC, abstractmethod
import scipy
from scipy.optimize import least_squares
from collections import defaultdict
import random

class MDP(ABC):
    def __init__(self, environment):
        self.environment = environment
        self.exitProgram = 0

    def bellman_value(self, current_state, action, value_function, gamma):
        state_value_ = 0
        for next_state in self.environment.possible_jumps(self.environment.A, current_state):
            movement_prob = self.environment.get_p(current_state, action, next_state)
            movement_reward = self.environment.get_r(current_state, action, next_state)
            state_value_ += movement_prob * (movement_reward + gamma * value_function.get(next_state, 0))
        return state_value_


    # Doesn't work when gamma = 1.0
    # Need to discount gamma, change value index
    def value_iteration(self, termination_epsilon = 0.01, gamma = 0.5):
        policy, value, value_delta = {}, {}, 1
        while value_delta > termination_epsilon:
            value_delta = 0
            last_value_function = value.copy()
            for state in self.environment.S:
                best_action, best_value = None, None
                for action in self.environment.possible_actions(state):
                    action_value = self.bellman_value(state, action, last_value_function, gamma)
                    
                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                value_delta = max(value_delta, abs(value.get(state, 0) - best_value))
                policy[state], value[state] = best_action, best_value
        return policy


    def policy_iteration(self, termination_epsilon = 0.01, gamma = 0.5):
        policy = {state : random.choice(self.environment.possible_actions(state)) for state in self.environment.S}
        value_function = {state : 0 for state in self.environment.S}

        while True:
            # Policy Evaluation
            value_delta = 1
            while value_delta > termination_epsilon:
                value_delta = 0
                last_value_function = value_function.copy()
                for state in self.environment.S:
                    state_value = self.bellman_value(state, policy[state], last_value_function, gamma)
                    value_delta = max(value_delta, abs(value_function[state] - state_value))
                    value_function[state] = state_value

            # Policy Improvement
            is_policy_stable = True 
            for state in self.environment.S:
                best_action, best_value = None, None
                for action in self.environment.possible_actions(state):
                    action_value = self.bellman_value(state, action, value_function, gamma)
                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                if policy[state] != best_action:
                    is_policy_stable = False

                policy[state] = best_action

            if is_policy_stable:
                break

        return policy
        
    def value_iteration_FA(self, termination_epsilon = 0.01, gamma = 0.5):
        policy, value, value_theta, value_delta = {}, {}, {}, 1
        theta = random.rand(#number of basis functions
        )

        while value_delta > termination_epsilon:
            value_delta = 0
            for state in self.environment.S:
                best_action, best_value = None, None
                for action in self.environment.A:
                    action_value = 0
                    for next_state in self.environment.S:
                        movement_prob = self.environment.P.get(state, {}).get(action, {}).get(next_state, 0)
                        movement_reward = self.environment.R[state][action][next_state]
                        action_value += movement_prob * (movement_reward + gamma * (theta * self.environment.calculate_phi(next_state)))
                    
                    if best_action is None or action_value > best_value:
                        best_action, best_value = action, action_value

                value_delta = max(value_delta, abs(value.get(state, 0) - best_value))
                policy[state], value[state] = best_action, best_value
            def v_difference(x):
                squared_sum = 0
                difference = 0
                for state in self.environment.S:
                    difference = value[state] - (x * self.environment.calculate_phi(state))
                    squared_sum =+ squared_sum + (difference * difference)
                return squared_sum
            ls_theta = least_squares(squared_sum, theta)
            theta = ls_theta.x
        return policy

    def print_value(self, value_function):
        print("Value: ")
        for i in range(len(self.environment.grid)):
            row = '|'
            for j in range(len(self.environment.grid[0])):
                row += f'{round(value_function[(i, j)], 2)}|'
            print(row)
