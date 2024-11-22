import pandas as pd

# Replace with the path to your CSV file
file_path = "SUB051 - CDP Job Seeker General-19112024.csv"

# Load the CSV file
data = pd.read_csv(file_path)

# Get and print the column names
print(data.columns.tolist())
