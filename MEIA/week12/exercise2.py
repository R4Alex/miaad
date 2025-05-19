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

[frame['Col3'] < 10]

pprint(frame)

import pdb; pdb.set_trace()