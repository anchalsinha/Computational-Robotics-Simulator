import numpy as np
import itertools as it
import math
from .base_environment import Environment


class YahtzeeEnvironment(Environment):
    def __init__(self, Pe):
        dice_possibilities = [1,2,3,4,5,6]
        self.num_dice = 5
        S = list(it.combinations_with_replacement(dice_possibilities, self.num_dice))
        A = list(it.product(range(1), repeat=self.num_dice))
        self.scores = self.score_rolls(S)
        P = self.calculate_transition_prob_set(S, A)
        R = self.calculate_reward_set(S, A)
        O = self.calculate_O(S)

        Environment.__init__(self, S, A, P, O, R)
    
    def possible_actions(self, next_state):
        return self.A 
    
    def possible_jumps(self, actions, curr_state):
        possible = []
        for a in actions:
            for ns in self.S:
                if self.P[curr_state][a][ns] != 0:
                    possible.append(ns)
        return possible
    
    def get_p(self, state, action, next_state):
        return self.P[state][action][next_state]

    def get_r(self, state, action, next_state):
        return self.R[state][action][next_state]
    
    def calculate_O(self, S):
        O = {}
        for s in S:
            O[s] = np.array([[1,1],[1,0]])
        return O

    def score_rolls(self, S):
        roll_scores = {}
        for state in S:
            s = np.asarray(state)
            counts = np.sort(np.bincount(s))
            scores = {}
            scores['chance']          = np.sum(s)
            scores['yahtzee']         = (len(set(s)) == 1) and 50 or 0
            scores['large_straight']  = (np.array_equal(np.asarray(range(s[0], s[0]+5)), s)) and 40 or 0
            scores['small_straight']  = (np.array_equal(np.asarray(range(s[0], s[0]+4)), np.unique(s))) and 30 or 0
            scores['three_of_a_kind'] = (counts[-1] >= 3) and s.sum() or 0
            scores['four_of_a_kind']  = (counts[-1] >= 4) and s.sum() or 0
            scores['full_house']      = (counts[-1] == 3 and counts[-2] == 2) and 25 or 0
            roll_scores[state] = max(scores.values())

        return roll_scores
    
    def calculate_reward_set(self, S, A):
        R = {}
        for state in S:
            R.setdefault(state, {})
            for action in A:
                R[state].setdefault(action, {})
                for next_state in S:
                    R[state][action][next_state] = self.scores[next_state] - self.scores[state]
        return R

    def calculate_transition_prob_set(self, S, A):
        T = {}

        for s in S:
            state = np.asarray(s)
            T.setdefault(s, {})
            for a in A:
                action = np.asarray(a)
                num_rolls = np.count_nonzero(action)
                T[s].setdefault(a, {})
                for ns in S:
                    next_state = np.asarray(ns)
                    keep = state[np.where(action==0)]
                    needed = np.copy(next_state)

                    for i in [v for v in keep if v in needed]:
                        del_i = (needed==i).argmax()
                        if needed[del_i] == i:
                            needed = np.delete(needed, del_i)
                    
                    '''
                    print(state)
                    print(action)
                    print(next_state)
                    print(keep)
                    print(needed)
                    print()
                    '''
                        
                    if len(needed) == num_rolls:
                        T[s][a][ns] = math.factorial(len(set(needed))) * ((1/6)**num_rolls)
                    else:
                        T[s][a][ns] = 0

        return T 
    
    def visualize(self, states, policy):
        print('Current state:')
        print(states[0])

        print('Policy:')
        print(policy[states[0]])
