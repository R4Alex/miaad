# 8. Scatter Plot
# Objective: Visualize the relationship between two variables.
# Instructions:
# Use the iris dataset from Seaborn.
# Create a scatter plot to visualize the relationship between sepal width (sepal_width) and sepal length (sepal_length).
# Add different colors based on the flower species.

import seaborn as sns
import matplotlib.pyplot as plt

# Apply the default theme
sns.set_theme()
# Load an example dataset
iris = sns.load_dataset("iris")
# Create scatter plot
sns.scatterplot(data=iris, x="sepal_width", y="sepal_length", hue="species", palette="Set2")
plt.xlabel("Sepal Width (cm)")
plt.ylabel("Sepal Length (cm)")
plt.savefig("image_exercise8.png")
