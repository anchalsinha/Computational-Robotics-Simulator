import numpy as np
import random
from scipy.misc import derivative
from scipy.integrate import quad 
import pdb
from utils.utils import Graph

from .base_environment import Environment

class NumberLineEnvironment(Environment):
    def __init__(self,planning_type='rrt',gamma = 0.8,hill_size=2,resolution=0.9,target_state= (0,0),v_max=10.0,y_max=10.0):
        self.v_max = v_max
        self.y_max = y_max
        self.p_c = 5
        self.m = 0.5
        self.hill_size = hill_size    #TODO make input
        self.input_UB = 1
        self.input_LB = -1
        self.planning_type = planning_type

        #MDP
        self.gamma = gamma
        self.resolution = resolution

        #prm
        self.prm_time_upper_bound = 2
        
        self.position = 0  # position
        self.velocity = 0  # velocity
        self.time = 0

        self.target_state = target_state

        if self.planning_type != 'rrt':
            self.state_space_discretization(self.resolution) # sets the position_space and velocity_space
            self.action_space_discretization()
            self.update_state()

            # define state and action spaces.We formulate based on aggregate sets
            S = [(y, x) for y in self.position_space for x in  self.velocity_space]  # set of all states
            A = self.action_space                                # set of all actions

            O = self.calculate_observation_set(S)            # set of all observations
            P = self.calculate_discrete_transition_probability_set(S, A)    # set of all transtions probabilities
            R = self.calculate_reward_set(S,A)

            Environment.__init__(self, S, A, P, O,R)
            print(len(self.P.keys()))

    def state_space_discretization(self,resolution= 0.1):
        self.position_space = np.arange(-self.y_max,self.y_max+resolution,resolution)
        self.velocity_space = np.arange(-self.v_max,self.v_max+resolution,resolution)

    def get_p(self,current_state, action, next_state):
        ##TODO add the prob determination via knn here
        retval = self.P[current_state][action][next_state]
        
        return retval

    def get_r(self,current_state, action, next_state):
        return self.R[current_state][action][next_state]

    def action_space_discretization(self,resolution=0.1):
        self.action_space = np.arange(self.input_LB,self.input_UB,resolution)

    def phi(self,y) -> int :
        """potential field"""
        return self.hill_size*np.sin((2*np.pi*y)/self.y_max)

    def sim_input(self, t):
        return 1

    def update_state(self):
        #TODO add  check to see if valid (?)
        self.state = (self.position,self.velocity)

    def calculate_reward_set(self, S, A):
        """
        Iterating through all the states in the state space
        ### Rewards
        - 1 for next state desired state
        - v-1 for next state undesired state
        """

        R = {}
        for state in S:
            for action in A:
                for next_state in S:
                    R.setdefault(state, {})
                    R[state].setdefault(action, {})
                    if next_state == self.target_state:
                        R[state][action][next_state] = 1
                    elif next_state != self.target_state:
                        R[state][action][next_state] = -1

        return R

    def calculate_observation_set(self,S) :
        O = {}
        for state in S:
            o =  self.h(state[0],state[1])
            O[state] = o
        return O

    def h(self,position=None,velocity=None) -> int:
        #observation of the velocity
        if position ==None:
            position=self.position
        if velocity == None:
            velocity =self.velocity
        retval =  int(position + self._noise_sensor(velocity))
        #check for bounds
        retval =self._check_bounds(retval,self.y_max)
        return retval

    def _check_bounds(self,retval,max_val):
        if retval > max_val:
            retval =max_val
        elif retval < -max_val:
            retval= -max_val
        return retval

    def _next_position(self,state):
        retval = state[0] + state[1]*1 #time step one unit (u+vt)
        return self._check_bounds(retval,self.y_max)

    def _next_velocity(self,state,action):
        """
        Velocity of next state \\
            - Influence of net force 
            - Influence of noise due to system dynamics
            - Checks bounds
        """
        next_velocity = state[1] + (1 / self.m) * self._net_force(action) + self._noise_dynamics(state[1])
        return self._check_bounds(next_velocity,self.v_max)

    def _next_state(self, state, action):
        has_crashed = random.uniform(0, 1) < ((np.abs(state[1])) * self.p_c)/self.v_max
        if has_crashed:
            next_velocity = 0.0
        else:
            next_velocity = self._next_velocity(state, action)
        next_position = self._next_position(state)
        next_state = (next_position, next_velocity)
        return next_state


 # np.linalg.norm(np.subtract(vertex, current))
       
    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def a_star(self, graph, start, goal):
        from queue import PriorityQueue
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph[current]:
                new_cost = cost_so_far[current] + self.heuristic(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    def bfs(self, graph, start, goal):
        from queue import Queue
        frontier = Queue()
        frontier.put(start)
        came_from = {start: True}

        while not frontier.empty():
            current = frontier.get()

            # Early exit
            if current == goal:
                break

            print('Visiting {}'.format(current))
            for next in graph[current]:
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = True

        return came_from

    def is_connected(self, n1, n2):
        x0, v0 = n1
        x, v = n2
        a = 2
        
        if x == x0 and v == v0:
            return True

        try:
            f_i = ((1/2)*self.m*v**2 - (1/2)*self.m*v0**2 - self.integrate_phi(x0,x)) / (x - x0)
        except ZeroDivisionError:
            f_i = 0

        return -1 <= f_i <= 1
    
    def integrate_phi(self,start,end):
        res,err = quad(self.phi,start,end)
        return res


    def drive(self, start, end):
        theta = np.arctan2(end[1] - start[1], end[0] - start[0])
        return start[0] + random.uniform(0, 10) * np.cos(theta), start[1] + random.uniform(0, 10) * np.cos(theta)

    def rrt1(self,start, end):
        G = Graph(start, end)

        # find random vertex
        # check for obstacles
        # 
        while i in range

    def rrt(self, start = (-10,-10), end= (0, 0)):
        start = tuple(start)
        end = tuple(end)

        vertices = {}
        vertices[start] = set()

        def get_nearest(vertex):
            distances = [(end_vertex, np.linalg.norm(np.subtract(vertex, end_vertex))) for end_vertex in vertices.keys()]
            return min(distances, key=lambda x: x[1])[0]

        while True:
            rand_vertex = random.uniform(-self.y_max , self.y_max), random.uniform(-self.v_max , self.v_max)
            nearest_vertex = get_nearest(rand_vertex)
            if (new_vertex := self.drive(nearest_vertex, rand_vertex)) is not None and self.is_connected(nearest_vertex, new_vertex):
                vertices[new_vertex] = set()
                vertices[nearest_vertex].add(new_vertex)
                if self.is_connected(new_vertex, end):
                    vertices[new_vertex].add(end)
                    break
        
        # came_from = self.bfs(vertices, start, end)
        came_from, _ = self.a_star(vertices, start, end)
        return self.reconstruct_path(came_from, start, end)

    def calculate_transition_prob_set(self,S, A):
        """Week 2 content"""
        transition_mat = {}
        for state in S: #current State
            a_dict = {}
            for action in A:  #current action
                s_dict = {}
                has_crashed = random.uniform(0, 1) < ((np.abs(state[1])) * self.p_c)/self.v_max
                if has_crashed:
                    next_velocity = 0
                else:
                    next_velocity = self._next_velocity(state, action)
                next_position = self._next_position(state)
                next_state = (next_position,next_velocity)
                s_dict[next_state] = 1 #transition probability 1 for now
                # calculate prob here, from the output of the sys dynamincs equation using it with the probability bins (another function) to calculate p, using knn

                a_dict[action] = s_dict
            transition_mat[tuple(state)] = a_dict
        return transition_mat

    def calculate_discrete_transition_probability_set(self, S, A):
        """Returns the transition probability matrix"""
        samples = 10
        discrete_transition_dict = {}
        # Initialize the probability set with zero
        print(len(S),len(A))
        # for state in S:
        #     for action in A:
        #         for new_state in S:
        #             discrete_transition_dict[(state,action,new_state)] = 0.0
        
        for state in S:
            a_dict = {}
            for action in A:
                s_dict = {}
                possible_next_states = {}
                for i in range(samples):
                    # iterate the system dynamics 100 times form (S(i),A(i))
                    next_state = self._next_state(state, action)
                    if next_state in possible_next_states:
                        possible_next_states[next_state] = possible_next_states[next_state] + self.resolution
                    else:
                        possible_next_states[next_state] = self.resolution
                
                # Populate the transition dictionary
                for a_next_state in possible_next_states:
                    normalized_prob = possible_next_states[a_next_state]/samples*100.0
                    s_dict[a_next_state] = normalized_prob
                    # discrete_transition_dict[(state,action,a_next_state)] = normalized_prob
                a_dict[action] = s_dict
            discrete_transition_dict[state]=a_dict
            # print(discrete_transition_dict)
        return discrete_transition_dict

    def _probability_of_state(self):
        pass

    def _knn(self):
        pass

    def possible_actions(self, present_state):
        ##TODO fit to numberline problem
        return self.A


    def _net_force(self, input_force) -> int:
        """The net force \\
           Input force + force exerted by loc in the potential field
        """
        f_net = int(input_force + derivative(self.phi, self.state[0]) )
        return f_net

    def _noise_sensor(self,v):
        return np.random.normal(0, np.abs(0.5*v))

    def _noise_dynamics(self,v):
        """
        Speed wobble dynamics
        """
        #TODO change to new speed wobble
        return np.random.normal(0, np.abs(0.1*v))

    def possible_actions(self,a):
        return self.A
    
    def possible_jumps(self,actions,state):
        return self.S

    # Overload
    def possible_actions(self, state):
        return self.A

    
    def LQR(self):
        pass

    ## PRM ###############
    ##---------------------------------------------------------
    # Two points in state space can be connected if there exists a constant input fi that drives the initial state to the final state (over some upper-bounded duration of time)

    def PRM(self):
        pass

    def _motion_edge(self,current_state,next_state,action):
        """
        Two points in state space can be connected if there exists a constant input fi that drives the initial state to the final state (over some upper-bounded duration of time)

        Input = f_net

        Return:
            True if transition exists \\
            False is not

        """
        for action in range(-1,1):
            next_position = self._next_position(current_state)
            next_velocity = self._next_velocity(current_state,action)