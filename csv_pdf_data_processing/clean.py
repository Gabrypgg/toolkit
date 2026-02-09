#this code cleares the csv by removing ""
import pandas as pd
import os

file_name = "Esiti_FULL.csv"
file_path = f"./outputs/{file_name}"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

output_dir = "./outputs/cleaned/"
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, file_name)
column = 'PUNTEGGIO'
df[column] = df[column].str.replace(",", ".")
print(df[column].dtype)
df.to_csv(output_filename, index=False)
print(f"\nSuccessfully saved cleaned data to '{output_filename}'")
