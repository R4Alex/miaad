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
