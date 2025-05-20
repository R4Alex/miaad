# 4. Time Series Analysis
# Objective: Work with dates and time series.
# Instructions:

# Create a DataFrame with a column of dates (use pd.date_range() to generate the dates).

# Generate 100 random values associated with these dates.

# Calculate the moving average of the values using a 5-day window.


import numpy as np
import pandas as pd
from pprint import pprint

frame = pd.DataFrame(columns=["dates", "values"])
frame["dates"] = pd.date_range(start="2025-05-01", periods=100, freq="D")
frame["values"] = np.array([np.random.randint(1, 51) for _ in range(100)])
frame["movil_mode_5_days"] = frame["values"].rolling(window=5).mean()
pprint(frame.head(20))
# pprint(frame)
