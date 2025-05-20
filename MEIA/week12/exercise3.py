# 3. Descriptive Statistics
# Objective: Apply basic statistical analysis.
# Instructions:

# Create a DataFrame with 100 random values between 0 and 50.

# Calculate the mean, median, and mode of the values.

# Find the minimum and maximum values in the DataFrame.

import numpy as np
import pandas as pd
from pprint import pprint

frame = pd.DataFrame(
    [
        np.array([np.random.randint(1, 51) for _ in range(100)])
    ],
)

pprint(frame)

print("\nDataframe Media: ", frame.mean(1).values)
print("Dataframe mode: ", frame.mode(1).values)
print("Dataframe mediam: ", frame.median(1).values)
print("Minimo: ", frame.min(1).values)
print("Maximo: ", frame.max(1).values)
