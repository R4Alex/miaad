# 2. DataFrame Operations
# Objective: Create and manipulate a DataFrame.
# Instructions:

# Create a DataFrame with 3 columns (A, B, C) and 5 rows of random integers.

# Rename the columns to Col1, Col2, Col3.

# Add a new column that is the sum of Col1 and Col2.

# Delete all rows where the value in Col3 is less than 10.

import numpy as np
import pandas as pd
from pprint import pprint

frame = pd.DataFrame(
    [
        np.array([np.random.randint(100) for _ in range(3)]) for _ in range(5)
    ],
    columns=["A", "B", "C"],
)

frame.columns=["Col1", "Col2", "Col3"]

frame["Col4"] = [value1 + value2 for value1, value2 in zip(frame["Col1"], frame["Col2"])]

pprint(frame)
print("")

frame = frame[frame['Col3'] > 10]

pprint(frame)
