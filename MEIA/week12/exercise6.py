# 6. Bar Chart
# 
# Objective: Visualize categorical data.
# Instructions:
# 
# Load the tips dataset from Seaborn.
# Create a bar chart showing the total bill amounts (total_bill) grouped by day.
# Add axis labels and a title.

import seaborn as sns
import matplotlib.pyplot as plt

# Apply the default theme
sns.set_theme()
# Load an example dataset
tips = sns.load_dataset("tips")
# Group by day
totals_by_day = tips.groupby("day")["total_bill"].sum().reset_index()
# Create Bar Chart
sns.barplot(data=totals_by_day, x="day", y="total_bill", color="skyblue")
# plt has the chart from sns, add labels and title
plt.xlabel("Day")
plt.ylabel("Total Bill")
plt.title("Total Bill by Day")
# Create a visualization
plt.savefig("image_exercise6.png")
