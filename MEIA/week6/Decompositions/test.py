import numpy as np
import scipy
from pprint import pprint


P = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0]
])

L = np.array([
    [1, 0, 0],
    [-1, 1, 0],
    [2, -5/4, 1],
])

U = np.array([
    [3, 6, 1],
    [0, 12, 29/2],
    [0, 0, 137/8],
])



B_recovered = np.dot(P, L)
B_recovered = np.dot(B_recovered, U)

print("\n(B) Matriz Original recuperada de la descomposicion:")
pprint(B_recovered)
