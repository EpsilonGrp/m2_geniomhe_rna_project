#Plot the epsilon distribution of the training set obtained through DSSR

import pandas as pd
import matplotlib.pyplot as plt

# Sample data
df = pd.read_csv('c:/Users/daphn/Downloads/RNA_project_DSSR/training.csv')

# Converting 'epsilon' column to numeric
df['epsilon'] = pd.to_numeric(df['epsilon'], errors='coerce')

# Dropping rows with NA values in the 'epsilon' column
df = df.dropna(subset=['epsilon'])

# Setting up the plot
plt.figure(figsize=(10, 6))
plt.hist(df['epsilon'], bins=range(-180, 181, 20), edgecolor='black', alpha=0.7)

# Setting plot labels and title
plt.xlabel('Epsilon Angle (degrees)')
plt.ylabel('Frequency')
plt.title('Histogram of Epsilon Angle')

# Showing grid
plt.grid(True)
