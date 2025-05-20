# 9. Heatmap
# Objective: Visualize the correlation between numerical variables.
# Instructions:
# Use the iris dataset from Seaborn.
# Calculate the correlation matrix of the variables.
# Create a heatmap to visualize the correlation matrix.

import seaborn as sns
import matplotlib.pyplot as plt

# Apply the default theme
sns.set_theme()
# Load an example dataset
iris = sns.load_dataset("iris")
correlation_matrix = iris.corr(numeric_only=True)
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.savefig("image_exercise9.png")
