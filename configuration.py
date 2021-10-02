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
P = 0.3

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
        jump_x = present_state[0] +a[0]
        jump_y = present_state[1] + a[1]
        if jump_x >= 0 and jump_x < rows and jump_y >= 0 and jump_y < cols:
            if grid[jump_x, jump_y] == '0' or grid[jump_x, jump_y] == 'S' or grid[jump_x, jump_y] == 'D':
                possible_jumps.append((jump_x, jump_y))
    return possible_jumps

def transition_matrix():
    # The states are represented from 1 to rows*cols using
    transition_mat = {}
    for s in S:
        list_possible_jumps = possible_jumps(s)
        a_dic ={}

        for a in A:
            s_dict = {}
            desired_state = s + a

            for s_ in S:
                if desired_state == s_ and s_ in list_possible_jumps:
                    s_dict[s_] = float(1-P)
                elif s_ in list_possible_jumps and s_ not in s_dict:
                    s_dict[s_] = P/4.0
                else:
                    s_dict[s_] = 0
            a_dic[a]= s_dict
        transition_mat[tuple(s)]  = a_dic
    return transition_mat

P = transition_matrix()