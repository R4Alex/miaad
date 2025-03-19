import numpy as np
import scipy
from pprint import pprint


B = np.array([
    [27/2, 6, -3],
    [3, 6, 1],
    [1, -3, 6]
])


# A = np.array([
#     [1, -3, 6],
#     [27/2, 6, -3],
#     [3, 6, 1],
# ])


P, L, U = scipy.linalg.lu(B)

print("(B) Matriz de entrada:")
pprint(B)
print("(P) Matriz Permutacion (identidad):")
pprint(P)
print("\n(L) Matriz Triangular Inferior:")
pprint(L)
print("\n(U) Matriz Triangular Superior:")
pprint(U)

B_recovered = np.dot(P, L)
B_recovered = np.dot(B_recovered, U)

print("\n(B) Matriz Original recuperada de la descomposicion:")
pprint(B_recovered)
