# Computational Robotics Simulator
This repository contains the abstract framework to simulate any discrete state space system, currently implemented for the numberline and gridworld toy problems.

## Getting Started
### Installation
Clone the repository and install dependencies by executing the following command:

    pip3 install -r requirements.txt

This project relies on numpy (for computation and mathematical representation) and pynput (for testing with keyboard interactions)

### How to run
Two top-level scripts define the execution for a specific simulator: numberline.py and gridworld.py
Run the simluator by simply executing them in the Python3 environment with no arguments:

    python3 gridworld.py
    python3 numberline.py

#### Gridworld
Three properties define the gridworld environment: the grid (i.e. walls, dimensions, etc.), the error probability (P_e), and the initial state (as the (y,x) coordinate). We require that the initial state resides in an empty cell, meaning the initial state cannot be a wall or road or target location.
All three of these properties will be defined in the 'gridworld.py' file

#### Numberline
TODO


## Architecture
This simulation framework follows an inheritence based framework, categorized into four classes:

Environment - This stores the configuration of the specific simulation environment (i.e. grid, Pe, etc) and calculates the system sets S, A, P, O and the reward set R. 

Simulation - This executes the actual transitions of the current state based on the environment parameters, storing the current state and determining the next state and observation based on an action. Derived simulation classes implement the abstract visualization functionality and any simulation-specific features (i.e. keyboard input for gridworld to select an action).

MDP Solver - Implements value iteration and policy iteration to select actions based on the reward set and simulation environment. This is a generic class able to support any simulation environment, and therefore has no derived variants.

Execution - Top level 'main' functions for each simulation. This stores the global configuration of the environment and actually run the simulation, MDP solver, etc.

### Extension
To extend this framework to support a new system simulation, three files must be added:

1. Environment. Create a derived class of Environment that calculates S, A, P, O, and R for the system. (see grid_world_environment.py and number_line_environment.py)
2. Simulation. Create a derived class of Simulation that implements the system-specific features and visualization. (see grid_world_simulator.py and number_line_simulator.py)
3. Execution. Create a top level function to run the simulation that defines all system configuration and runs the simulator. (see gridworld.py and numberline.py)

## References
Mathematical formalisms and pseudocode: https://www.overleaf.com/project/61564dd5d8ef6b1302066d84