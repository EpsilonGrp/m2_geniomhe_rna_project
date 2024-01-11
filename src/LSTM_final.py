# -*- coding: utf-8 -*-
"""Baby2with_Masking_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZwfdXf6xzOcZElScYVrg3QV6RKExTVX0

# LSTM for prediction of epsilon angles of RNA


## Method Used : Keras

## Import Libraries
"""

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

"""## Load Dataset"""

# Upload the CSV file
uploaded = files.upload()

# Assuming you uploaded 'training_with_classes.csv'
file_path = 'New_training1.csv'
df = pd.read_csv(file_path)

"""Preprocessing"""

df.head(10)

from sklearn.preprocessing import LabelEncoder

# Assuming 'class' is your target variable
target_variable = 'class'

# Create a label encoder
label_encoder = LabelEncoder()

# Apply label encoding to 'class' column
df[target_variable] = label_encoder.fit_transform(df[target_variable])

print(df.info())

df['class'].isnull().sum()

# Check the updated DataFrame
df.head(100)

"""# split a multivariate sequence into samples"""

def split_sequences(sequences, n_steps):
	X, y = list(), list()

	for i in range(len(sequences)):
		# find the end of this subsequence
		end_ix = i + n_steps
		# check if we are beyond the sequence
		if end_ix > len(sequences)-1:
			break
		# combine input and output parts of the subsequence
		seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)

def split_sequences(sequences, n_steps):
    X, y = list(), list()

    for i in range(len(sequences)):
        # find the end of this subsequence
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequences)-1:
            break
        # combine input and output parts of the subsequence
        seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

"""# Split the dataset into train and test sets

## Creating the Model
** You can apply the different deep learning tools that allow to improve the results **

Built a LSTM model with 1 hidden layer.

Every LSTM layer should be accompanied by a Dropout layer. This layer will help to prevent overfitting.
"""

# Import necessary libraries
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout,SimpleRNN
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error

from keras.layers import Masking

map={
    '1' : -174.5,
    '2' : -165.5,
    '3' : -158.5,
    '4' : -150.5,
    '5' : -144.0,
    '6' : -139.0,
    '7' : -134.5,
    '8' : -127.5,
    '9' : -113.5,
    '10' : -80.5,
    '11' : 53.5,
    '12' : 171.5,
    '13' : 185.0,

    }

# Data cleaning
# Assuming 'class' is your target variable

df['class'] = df['class'].replace('Na', '13')
df['class'] = df['class'].astype(int)

#Defining features
input_features = ['A','C','G','U','rank']
X = df[input_features].values

#Defining target variable
target_variable = 'class'
y = df[target_variable].values

# Data splitting
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Creating the Neural Network

model = Sequential()
model.add(Masking(mask_value=0.0, input_shape=(None, x_train.shape[1])))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1, activation='softmax'))
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

# Reshape x_train and x_test to be 3D: (samples, time_steps, features)
x_train_reshaped = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
x_test_reshaped = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))

# Fit the model
model.fit(x_train_reshaped , y_train, epochs=400, verbose=1)

#Defining Mean Absolute Error function

def calculate_mae(epsilon_truth,y_pred):
  sum=0
  for i in range(len(y_pred)):
    di=np.abs(map[str(y_pred[i])]-epsilon_truth[i])
    ae=min(di,360-di)
    sum+=ae

  return sum/len(y_pred)

# Evaluate the model on the test set
score = model.evaluate(x_test, y_test, verbose=1)
print("Scores mse", score)

# Predictions
trainPredict_scaled = model.predict(x_train_reshaped)
testPredict_scaled = model.predict(x_test_reshaped)

# Inverse transform the predictions
trainPredict = scaler_y.inverse_transform(trainPredict_scaled)
testPredict = scaler_y.inverse_transform(testPredict_scaled)

# Plot baseline and predictions for the training set
plt.xlabel('Time')
plt.ylabel('Values')
plt.plot(y_train.flatten(), label='target')
plt.plot(trainPredict.flatten(), label='prediction')
plt.legend()
plt.show()

# Plot baseline and predictions for the test set
plt.xlabel('Time')
plt.ylabel('Values')
plt.plot(y_test.flatten(), label='target')
plt.plot(testPredict.flatten(), label='prediction')
plt.legend()
plt.show()

# Calculate MAE for training set
mae_train = calculate_mae(y_train.flatten(), trainPredict.flatten())
print(f"Mean Absolute Error (MAE) - Training Set: {mae_train}")

# Calculate MAE for test set
mae_test = calculate_mae(y_test.flatten(), testPredict.flatten())

# Save the model
model.save('modelLSTMRNA')

import os
import json
import pandas as pd
from tensorflow.keras.models import load_model

# Replace 'your_model_path.h5' with the path to your saved Keras model file
#model_path = 'modelLSTMRNA'

# Load the Keras model
#model = load_model(model_path)

class AngleHelper:
  def __init__(self,model):

    # Given that the trained model is previously loaded and passed as an argument
    self.model=model
    self.classes= {
    '1' : -174.5,
    '2' : -165.5,
    '3' : -158.5,
    '4' : -150.5,
    '5' : -144.0,
    '6' : -139.0,
    '7' : -134.5,
    '8' : -127.5,
    '9' : -113.5,
    '10' : -80.5,
    '11' : 53.5,
    '12' : 171.5,
    '13' : 185.0
    }



  def predict(self, in_path: str, out_path: str):
    """
    Function that should predict the angles for the sequence of nucleotides
    Args:
      - in_path: path to a `fasta` file.
        Example:
          "
          >17EP
          ACGUUCU
          "
      - out_path: path to a `.json` file where will be stored the prediciton.
        It should have the following keys: (example with `alpha` angle)
          {
            "17EP": {
              "sequence": "ACGUUCU",
              "angles": {"alpha": [0, 0, 0, 0, 0, 0, 0]}
            }

          }
    """
    name = None
    sequence = ""

    # Read the FASTA file
    with open(in_path, 'r') as file:
        # Iterate over lines in the file
        for line in file:
            # Skip lines starting with '>' as they are headers
            if line.startswith('>'):
                name = line.strip()[1:]  # Remove '>' and leading/trailing whitespaces
            else:
                sequence += line.strip()

    #Creaton of the output dictionnary
    output={}
    output[name]= {
              'sequence': sequence,
              "angles": {}
            }


    #Creation of the input data from the fasta file

    df = pd.DataFrame(columns=['A', 'G', 'C', 'U', 'rank'])

    # Fill the DataFrame based on the sequence
    for i, char in enumerate(sequence, start=1):
        row = {'A': 0, 'G': 0, 'C': 0, 'U': 0, 'rank': i}
        row[char] = 1
        df = df.append(row, ignore_index=True)

    # Convert the DataFrame to a NumPy array
    data_array = df[['A', 'G', 'C', 'U','rank']].astype(int).values
    data_array = data_array.reshape((data_array.shape[0], 1, data_array.shape[1]))


    #Predict the encoded classes
    encoded_pred=self.model.predict(data_array)


    #Convert them into angles
    epsilon=[]
    for prediction in encoded_pred:
      epsilon.append(self.classes[(str(int(np.ceil(prediction[0]))))])
    output[name]["angles"]["epsilon"]=epsilon

    #Save the dictionnary in a json file
    with open(out_path, 'w') as json_file:
      json.dump(output, json_file, indent=2)


    return None

if __name__ == "__main__":
    # Example of usage
    in_path = os.path.join("example.fasta")
    out_path = "sample.json"
    angle_helper = AngleHelper(model)
    angle_helper.predict(in_path, out_path)

"""## Results Visualisation"""

# Plot baseline and predictions for the training set
plt.xlabel('Time')
plt.ylabel('Values')
plt.plot(y_train[:, 0], label='target')  # Change here
trainPredict = (model.predict(x_train_reshaped))[:, 0]  # Change here
plt.plot(trainPredict, label='prediction')
plt.legend()
plt.show()

# Plot baseline and predictions for the test set
plt.xlabel('Time')
plt.ylabel('Values')
plt.plot(y_test[:, 0], label='target')  # Change here
testPredict = (model.predict(x_test_reshaped))[:, 0]  # Change here
plt.plot(testPredict, label='prediction')
plt.legend()
plt.show()

"""# Sample Test"""

sequence = input("Enter the sequence: ").upper()

nucleotide_vector = list(sequence)
rank = list(range(1, len(nucleotide_vector) + 1))

df2= pd.DataFrame({'sequence': nucleotide_vector})
df2['A'] = (df2['sequence'] == 'A').astype(int)
df2['C'] = (df2['sequence'] == 'C').astype(int)
df2['G'] = (df2['sequence'] == 'G').astype(int)
df2['U'] = (df2['sequence'] == 'U').astype(int)
df2=df2[['A','C','G','U']]
df2