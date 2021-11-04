import numpy as np
A = np.array([[1, 1], [0, 1]])
B = np.array([[0], [1]])

Q = np.array([[1, 0], [0, 1]])
R = np.array([[1]])
N = np.array([[0], [0]])

P = Q
iterations = 1000 
for i in range(iterations):
    P_new = A.T @ P @ A - (A.T @ P @ B + N) @ np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A + N.T) + Q
    if np.linalg.norm(P - P_new) < 1:
        break
    P = P_new

F = np.linalg.inv(R + B.T @ P @ B) @ (B.T @ P @ A + N.T)
print(F)

