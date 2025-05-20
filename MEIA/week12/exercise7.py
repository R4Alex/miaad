# 7. Histogram
# Objective: Visualize the distribution of numerical data.
# Instructions:
# Generate 1,000 random numbers with a normal distribution (mean = 0, standard deviation = 1).
# Create a histogram to visualize the distribution.
# Adjust the number of bins in the histogram to make the visualization clear.

import numpy as np
import matplotlib.pyplot as plt

def plot_histogram(values, title):
    plt.hist(values, bins=30, density=True, edgecolor='black')
    plt.title(title)
    plt.xlabel("Generated Value")
    plt.ylabel("Relative Frecuency")
    plt.grid(True)
    plt.savefig("%s.png" % title)

data = np.random.normal(loc=0, scale=1, size=1000)
plot_histogram(data, "image_exercise7")
