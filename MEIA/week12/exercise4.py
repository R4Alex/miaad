import numpy as np
import pandas as pd
from pprint import pprint

frame = pd.DataFrame(
    [
        np.array([np.random.randint(1, 51) for _ in range(100)])
    ],
)
