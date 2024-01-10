import json
import csv
import matplotlib.pyplot as plt

def extract_epsilon_angles(json_data):
    epsilon_angles = []
    
    for key, value in json_data.items():
        if "angles" in value and "epsilon" in value["angles"]:
            sequence = value.get("sequence", "")
            epsilon_values = value["angles"]["epsilon"]
            
            for i, nucleotide in enumerate(sequence):
                epsilon_angles.append({"nucleotide": nucleotide, "epsilon": epsilon_values[i]})
    
    return epsilon_angles

def save_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ["nucleotide", "epsilon"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def plot_histogram(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        epsilon_values = [float(row['epsilon']) for row in reader]
    
    plt.hist(epsilon_values, bins=range(-180, 181, 1), edgecolor='orange', alpha=0.7)
    plt.xlabel('Epsilon Angle')
    plt.ylabel('Frequency')
    plt.title('Distribution of Epsilon Angles')
    plt.show()

if __name__ == "__main__":
    # Read JSON data from file
    json_file_path = '../../data/test.json'
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    
    # Extract epsilon angles and save to CSV
    epsilon_data = extract_epsilon_angles(json_data)
    csv_file_path = '../../data/output.csv'
    save_to_csv(epsilon_data, csv_file_path)
    
    # Plot histogram
    plot_histogram(csv_file_path)

