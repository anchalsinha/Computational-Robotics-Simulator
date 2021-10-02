from sys import _debugmallocstats
import numpy as np
grid = np.array([
    [0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 'D', 0, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 'S', 0, 1],
])
# define state and action spaces
rows = 5
cols = 5
S = [(y, x) for y in range(0, rows) for x in range(0, cols)]
A = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]

# define P and O
Pe = 0.3

O = {}
Rd_loc = [2, 2]
Rs_loc = [4, 2]
def output(state):
    dD = np.linalg.norm(state - Rd_loc)
    dS = np.linalg.norm(state - Rs_loc)
    h = 2/((1/dD) + (1/dS))
    o = [[np.ceil(h), 1 - (np.ceil(h) - h)], [np.floor(h), np.floor(h) - h]]

# for s in S:
#     O[s] = output(s)
transition_matrix = {}

def possible_jumps(present_state):
    possible_jumps= []
    for a in A:
        jump_y = present_state[0] + a[0]
        jump_x = present_state[1] + a[1]
        if jump_y >= 0 and jump_y < rows and jump_x >= 0 and jump_x < cols:
            if grid[jump_y, jump_x] == '0' or grid[jump_y, jump_x] == 'S' or grid[jump_y, jump_x] == 'D':
                possible_jumps.append((jump_y, jump_x))
    return possible_jumps

def transition_matrix():
    # The states are represented from 1 to rows*cols using
    transition_mat = {}
    for s in S:
        if grid[s] == '1':
            continue

        list_possible_jumps = possible_jumps(s)
        a_dic ={}

        for a in A:
            s_dict = {}
            desired_state = tuple(np.add(s, a))
            invalid = tuple(desired_state) not in list_possible_jumps # check if desired state is invalid

            print(f'State: {s}, Action: {a}, Desired: {desired_state}, all: {list_possible_jumps}')

            for s_ in S:
                if invalid and s_ == s: # if invalid desired state and s_ is current state
                    print('Case 1')
                    s_dict[s_] = 1
                elif not invalid and desired_state == s_: # if not invalid desired state and s_ is desired state
                    s_dict[s_] = float(1-Pe)
                    print('Case 2')
                elif not invalid and s_ in list_possible_jumps: # if not invalid desired state and s_ is valid
                    s_dict[s_] = Pe/(len(list_possible_jumps)-1)
                    print('Case 3')
                else:
                    s_dict[s_] = 0
            a_dic[a]= s_dict
        transition_mat[tuple(s)]  = a_dic
    return transition_mat

P = transition_matrix()