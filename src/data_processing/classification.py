import pandas as pd
import matplotlib.pyplot as plt

# Data
df = pd.read_csv('../../RNA_project_DSSR/test.csv')

# Converting 'epsilon' column to numeric
df['epsilon'] = pd.to_numeric(df['epsilon'], errors='coerce')

# Dropping rows with NA values in the 'epsilon' column
df = df.dropna(subset=['epsilon'])


# Definition the threshold values for epsilon
threshold_C1 = -169.0
threshold_C2 = -162.0
threshold_C3 = -155.0
threshold_C4 = -146.0
threshold_C5 = -142.0
threshold_C6 = -136.0
threshold_C7 = -133.0
threshold_C8 = -122.0
threshold_C9 = -105.0
threshold_C10 = -56.0
threshold_C11 = 163.0
threshold_C12 = 180.0

# Function to assign class based on epsilon value
def assign_class(epsilon):
    if epsilon < threshold_C1:
        return '1'
    elif threshold_C1 <= epsilon < threshold_C2:
        return '2'
    elif threshold_C2 <= epsilon < threshold_C3:
        return '3'
    elif threshold_C3 <= epsilon < threshold_C4:
        return '4'
    elif threshold_C4 <= epsilon < threshold_C5:
        return '5'
    elif threshold_C5 <= epsilon < threshold_C6:
        return '6'
    elif threshold_C6 <= epsilon < threshold_C7:
        return '7'
    elif threshold_C7 <= epsilon < threshold_C8:
        return '8'
    elif threshold_C8 <= epsilon < threshold_C9:
        return '9'  
    elif threshold_C9 <= epsilon < threshold_C10:
        return '10' 
    elif threshold_C10 <= epsilon < threshold_C11:
        return '11'  
    elif threshold_C11 <= epsilon <= threshold_C12:
        return '12' 
    else:
        return 'Na'

# Application of the function to create the 'Class' column
df['class'] = df['epsilon'].apply(assign_class)

# Saving of the updated DataFrame to a new CSV file
df.to_csv('../../RNA_project_DSSR/test_with_classes.csv', index=False)




