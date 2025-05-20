# 5. Line Plot
# Objective: Visualize the trend of a data series.
# 
# Instructions:
# 
# Create a random data series (values between 0 and 100) of size 50.
# Use Matplotlib to plot the data as a line chart.
# Add a title, axis labels, and a legend.
# Change the line color to red and use a dashed line style.

import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

values = np.array([np.random.randint(101) for _ in range(50)])
plt.plot(values, color="red", linestyle="--")
plt.title("Exercise 5")
plt.ylabel("Random Values")
plt.xlabel("Order")
plt.legend(["Generated Values"], loc="lower left")
plt.savefig("image_exercise5.png")
