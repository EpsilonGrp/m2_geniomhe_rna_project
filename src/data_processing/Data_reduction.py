
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from google.colab import files
from sklearn.preprocessing import StandardScaler

# Upload the CSV file
uploaded = files.upload()

# Assuming you uploaded 'training_with_classes.csv'
file_path = '../../RNA_project_DSSR/training_with_classes.csv'
df = pd.read_csv(file_path)

df

# Upload the CSV file
uploaded = files.upload()

# Assuming you uploaded 'training_with_classes.csv'
file_path = '../../RNA_project_DSSR/test_with_classes.csv'
df1 = pd.read_csv(file_path)

input_features = ['rank', 'sequence', 'name', 'epsilon', 'class']
X = df[input_features]

X.head(10)

df1.head(10)

X1 = df1[input_features]
X1

X['A'] = (X['sequence'] == 'A').astype(int)
X['C'] = (X['sequence'] == 'C').astype(int)
X['G'] = (X['sequence'] == 'G').astype(int)
X['U'] = (X['sequence'] == 'U').astype(int)

column_order = ['rank', 'sequence', 'A', 'C', 'G', 'U', 'name', 'epsilon', 'class']

X = X[column_order]

X = X.drop(columns=['sequence'])

X

X1.isna().any()

len(X['name'].unique())

X1['A'] = (X1['sequence'] == 'A').astype(int)
X1['C'] = (X1['sequence'] == 'C').astype(int)
X1['G'] = (X1['sequence'] == 'G').astype(int)
X1['U'] = (X1['sequence'] == 'U').astype(int)

X1 = X1[column_order]

X1 = X1.drop(columns=['sequence'])

X1

X.to_csv('../../data/New_training.csv', index=False)
X1.to_csv('../../data/New_test.csv', index=False)