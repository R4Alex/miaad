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


Q, R = scipy.linalg.qr(B)

print("(B) Matriz de entrada:")
pprint(B)
print("(Q) Matriz Ortonormal:")
pprint(Q)
print("\n(R) Matriz Triangular Superior:")
pprint(R)

B_recovered = np.dot(Q,R)

print("\n(B) Matriz Original recuperada de la descomposicion:")
pprint(B_recovered)
