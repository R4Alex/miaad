# 1. Basic Operations
# Objective: Create and manipulate arrays.
# Instructions:

# Create an array with 10 elements containing values from 1 to 10.

# Calculate the mean, median, and standard deviation of the values.

# Multiply each value by 2.

import numpy as np
from pprint import pprint

array = np.array([np.random.randint(1, 11) for _ in range(10)])
pprint(array)

print("Media: ", (sum(array)/len(array)))
print("Desviacion estandar: ", (np.std(array)))

new_array =  np.array([value*2 for value in array])
pprint(new_array)
