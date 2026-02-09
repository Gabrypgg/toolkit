#this code allows to plot data in ./outputs/cleaned folder

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

filename = "Esiti_FULL.csv"
file_dir = f"./outputs/cleaned/{filename}"
def plot_punteggio_distribution(file_dir):
    """
    Loads a CSV file and plots the distribution of the 'PUNTEGGIO' column.
    """
    minimum_score = 25.1
    try:
        # --- 1. Load Data ---
        print(f"Loading data from '{file_dir}'...")
        df = pd.read_csv(file_dir)
        print("Data loaded successfully.")

        # --- 2. Validate Data ---
        if 'PUNTEGGIO' not in df.columns:
            print(f"Error: 'PUNTEGGIO' column not found in {file_dir}", file=sys.stderr)
            print(f"Available columns are: {df.columns.tolist()}", file=sys.stderr)
            return
        
        # Ensure PUNTEGGIO is numeric, converting any non-numeric values to NaN (and dropping them)
        df['PUNTEGGIO'] = pd.to_numeric(df['PUNTEGGIO'], errors='coerce')
        initial_count = len(df)
        df = df.dropna(subset=['PUNTEGGIO'])
        dropped_count = initial_count - len(df)
        if dropped_count > 0:
            print(f"Warning: Dropped {dropped_count} rows with non-numeric or missing PUNTEGGIOs.")

        if df.empty:
            print("Error: No valid PUNTEGGIO data to plot.", file=sys.stderr)
            return

        #Taking only people with score > 21
        df = df.loc[df.iloc[:,1].ge(minimum_score),:]
        print(df)
        print(f"Il numero totale di Idonei (voto > {minimum_score}) è: {len(df)}")

        # --- 3. Plotting ---

        # --- Method 1: Histogram (Recommended for continuous float data) ---
        # This groups PUNTEGGIOs into bins and shows the frequency.
        print("Generating histogram...")
        plt.figure(figsize=(12, 7))
        # kde=True adds a smooth line (Kernel Density Estimate) over the bars
        sns.histplot(df['PUNTEGGIO'], bins=30, kde=True, color='blue', edgecolor='black')
        plt.title(f'Distribution of PUNTEGGIOs (from {file_dir})', fontsize=16)
        plt.xlabel('PUNTEGGIO', fontsize=12)
        plt.ylabel('Frequency (Number of IDs)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        print("Displaying plot. Close the plot window to exit.")
        plt.show()


        # --- Method 2: Bar Chart (Good if you have few, specific PUNTEGGIO values) ---
        # This counts each unique PUNTEGGIO value.
        # Uncomment the block below and comment out Method 1 to use this.
        
        print("Calculating value counts for bar plot...")
        PUNTEGGIO_counts = df['PUNTEGGIO'].value_counts().sort_index()
        # Add a check to prevent plotting if there are too many unique PUNTEGGIOs
        max_unique_PUNTEGGIOs = 50 
        if len(PUNTEGGIO_counts) > max_unique_PUNTEGGIOs:
            print(f"\nNote: Skipped bar plot because there are {len(PUNTEGGIO_counts)} unique PUNTEGGIOs.")
            print(f"The histogram (Method 1) is better for this type of data.")
            print(f"Top 20 most common PUNTEGGIOs:\n{PUNTEGGIO_counts.nlargest(20)}")

            #Save distribution
            output_dir = "./outputs/distribution/"
            os.makedirs(output_dir, exist_ok=True)
            PUNTEGGIO_counts.to_csv(f"{output_dir}/counts.csv")

        else:
            print("Generating bar plot...")
            plt.figure(figsize=(12, 7))
            PUNTEGGIO_counts.plot(kind='bar', color='skyblue', edgecolor='black')
            plt.title(f'Frequency of Each PUNTEGGIO (from {file_dir})\n Minimum score: {minimum_score}', fontsize=16)
            plt.xlabel('PUNTEGGIO', fontsize=12)
            plt.ylabel('Frequency (Number of IDs)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            print("Displaying plot. Close the plot window to exit.")
            plt.show()


    except FileNotFoundError:
        print(f"Error: The file '{file_dir}' was not found.", file=sys.stderr)
        print("Please make sure the file is in the same directory as the script.", file=sys.stderr)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_dir}' is empty.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    plot_punteggio_distribution(file_dir)