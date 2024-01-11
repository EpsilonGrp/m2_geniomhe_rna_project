import os
import json
import pandas as pd

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
    data_array = df[['A', 'G', 'C', 'U','rank']].to_numpy()

    #Predict the encoded classes
    encoded_pred=self.model.predict(data_array)

    #Convert them into angles
    epsilon=[]
    for prediction in encoded_pred:
      epsilon.append(self.classes(str(prediction)))
    
    output[name]["angles"]["epsilon"]=epsilon

    #Save the dictionnary in a json file
    with open(out_path, 'w') as json_file:
      json.dump(output, json_file, indent=2)
    
    
    return None

if __name__ == "__main__":
    # Example of usage
    in_path = os.path.join("data", "sample", "example.fasta")
    out_path = "sample.json"
    angle_helper = AngleHelper()
    angle_helper.predict(in_path, out_path)