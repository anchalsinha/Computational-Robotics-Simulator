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
#S = np.array([(x, y) for x in range(0, rows) for y in range(0, cols)])
#A = np.array([(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)])
S = [(x, y) for x in range(0, rows) for y in range(0, cols)]
A = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]


A_indices = [1,2,3,4,0]
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
def convert_index(i,j):
    return int( i*rows + j)

def possible_jumps(present_state):
    possible_jumps= []
    for a in A:
        jump_x = present_state[0] +a[0]
        jump_y = present_state[1] + a[1]
        print(jump_x, jump_y)
        if jump_x >= 0 and jump_x < rows and jump_y >= 0 and jump_y < cols:
            if grid[jump_x, jump_y] == '0' or grid[jump_x, jump_y] == 'S' or grid[jump_x, jump_y] == 'D':
                possible_jumps.append([jump_x, jump_y])
    return possible_jumps

def transition_matrix():
    # The states are represented from 1 to rows*cols using
    transition_mat = {}
    for s in S:
        sindex = convert_index(s[0], s[1])
        print( 's ', s,' sindex ', sindex)

        list_possible_jumps=possible_jumps(s)
        possible_jump_indices = []
        for jump in list_possible_jumps:
            possible_jump_indices.append(convert_index(jump[0], jump[1]))
        a_dic ={}
        print("possible jumps",possible_jump_indices)
        for a in A_indices:
            s_dict={}
            #print('inidces of A',A_indices.index(a), 'a is ',a)
            desired_state = (s[0] + A[A_indices.index(a)][0], s[1] +A[A_indices.index(a)][1])
            desired_state_index = convert_index(desired_state[0], desired_state[1])

            for s_ in S:
                s_index = convert_index(s_[0], s_[1])
                if desired_state_index == s_index and s_index in possible_jump_indices :
                    print("added for the 1-p", s_index, " for action ", a)
                    s_dict[s_index] =  float(1-P)

                elif s_index in possible_jump_indices and s_index not in s_dict:
                    print("added present index p/4", s_index)
                    s_dict[s_index] = P/4.0
                else:
                    s_dict[s_index] =0
            a_dic[a]= s_dict
        transition_mat[sindex]  = a_dic
    return transition_mat

trans = transition_matrix()
test_index_s = (1,0)
test_index_s_ = (0,0)
action = (1,0)
#print(trans[20][3])
## directly give the input interms of (s,a,s')
print(trans[convert_index(test_index_s[0], test_index_s[1])][A_indices[A.index(action)]][convert_index(test_index_s_[0], test_index_s_[1])])
