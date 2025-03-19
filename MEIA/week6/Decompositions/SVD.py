import numpy as np
import scipy
from pprint import pprint

# B = np.array([
#     [27/2, 6, -3],
#     [3, 6, 1],
#     [1, -3, 6]
# ])

B = np.array([
    [1, -3, 6],
    [27/2, 6, -3],
    [3, 6, 1],
])

U, S, VH = scipy.linalg.svd(B)


print("(B) Matriz de entrada:")
pprint(B)
print("(U) Matriz ortonormal izquierda:")
pprint(U)
print("\n(S) Matriz diagonal con los valores singulares:")
pprint(S)
print("\n(VH) Matriz ortonormal derecha transpuesta:")
pprint(VH)


# Acomodar como matriz de nuevo, para poder multiplicarla
S = np.array([
    [S[0], 0, 0],
    [0, S[1], 0],
    [0, 0, S[2]]
])

B_recovered = np.dot(U, S)
B_recovered = np.dot(B_recovered, VH)

print("\n(B) Matriz Original recuperada de la descomposicion:")
pprint(B_recovered)
