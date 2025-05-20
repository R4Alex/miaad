# 10. Line Plot with Moving Average
# Objective: Visualize time series data.
# Instructions:
# Generate a time series of 100 days with random values.
# Calculate the 10-day moving average and plot it alongside the original series.
# Use different colors for the original series and the moving average.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates  = pd.date_range(start="2025-01-01", periods=100, freq="D")
values = np.random.rand(100) * 100
frame = pd.DataFrame({"dates": dates, "values": values})
frame['movil_mode_5_days'] = frame['values'].rolling(window=10).mean()

plt.figure(figsize=(12, 6))
plt.plot(frame["dates"], frame["values"], label="Original Series", color="blue")
plt.plot(frame["dates"], frame["movil_mode_5_days"], label="Mobile Media (10 days)", color="orange")

plt.title("Mobile Media (10 days)")
plt.xlabel("Dates")
plt.ylabel("Values")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("image_exercise10.png")
