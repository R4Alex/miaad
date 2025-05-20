# 11. Time Series with Statistical Analysis
# Objective: Work with time series and compute statistics.
# Instructions:
# Generate a time series of 200 days with random values.
# Calculate the mean and standard deviation of the time series.
# Visualize the series along with the standard deviation bands (i.e., mean ± 1 standard deviation).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Generate a time series of 200 days with random values
dates = pd.date_range(start="2025-01-01", periods=200, freq="D")
values = np.random.rand(200) * 100  # random values between 0 and 100
df = pd.DataFrame({'Date': dates, 'Value': values})
# 2. Calculate the mean and standard deviation
mean = df['Value'].mean()
std_dev = df['Value'].std()
# 3. Plot the time series with standard deviation bands
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Value'], label='Time Series', color='blue')
plt.axhline(mean, color='green', linestyle='--', label='Mean')
plt.axhline(mean + std_dev, color='red', linestyle='--', label='Mean + 1σ')
plt.axhline(mean - std_dev, color='red', linestyle='--', label='Mean - 1σ')
# Add labels and title
plt.title("Time Series with Standard Deviation Bands")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("image_exercise11.png")
