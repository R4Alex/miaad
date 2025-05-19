import numpy as np
from pprint import pprint

array = np.array([np.random.randint(1, 11) for _ in range(10)])
pprint(array)

print("Media: ", (sum(array)/len(array)))
print("Desviacion estandar: ", (np.std(array)))

new_array =  np.array([value*2 for value in array])
pprint(new_array)
