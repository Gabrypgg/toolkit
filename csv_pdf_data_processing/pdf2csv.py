# pip install pdfplumber
#this code extracts tables in the given pdf, and trasforms in a csv only the values defined in header

import pdfplumber
import csv
import sys

# --- CONFIGURATION ---
# 1. SET YOUR PDF FILE PATH HERE
pdf_path = './inputs/Esiti_single.pdf'  # <--- IMPORTANT: Change this to the name of your PDF

# 2. SET YOUR DESIRED OUTPUT CSV FILE NAME
csv_path = './outputs/Esiti_single.csv'
# ---------------------

# The headers we are looking for
HEADER_1 = 'CODICE CANDIDATURA'
HEADER_2 = 'PUNTEGGIO'

def extract_data_from_pdf(pdf_file_path):
    """
    Extracts data from tables in a PDF file based on specific headers.
    """
    all_data = []
    codice = HEADER_1
    punteggio = HEADER_2
    all_data.append([codice, punteggio])
    
    print(f"Opening PDF: {pdf_file_path}...")
    
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            print(f"PDF has {len(pdf.pages)} pages.")
            
            # Loop through each page in the PDF
            for i, page in enumerate(pdf.pages):
                print(f"\nProcessing Page {i + 1}...")
                
                # Extract all tables from the current page
                # .extract_tables() returns a list of tables
                tables = page.extract_tables()
                
                if not tables:
                    print(f"No tables found on Page {i + 1}.")
                    continue
                
                print(f"Found {len(tables)} table(s) on Page {i + 1}.")
                
                # Process each table found on the page
                for table in tables:
                    if not table:
                        print("Skipping an empty table block.")
                        continue
                    
                    # The first row is assumed to be the header
                    header_row = table[1]
                    
                    # Try to find the column index for our desired headers
                    try:
                        codice_idx = header_row.index(HEADER_1)
                        punteggio_idx = header_row.index(HEADER_2)
                        print(f"Found headers: '{HEADER_1}' (Col {codice_idx}) and '{HEADER_2}' (Col {punteggio_idx}).")
                    except ValueError:
                        # If headers aren't found, print a warning and skip this table
                        print(f"Warning: Could not find required headers in a table on Page {i + 1}. Skipping table.")
                        print(f"Found headers: {header_row}")
                        continue
                    
                    # Loop through the rest of the rows (skip the header row)
                    for row in table[2:]:
                        # Ensure the row has enough columns
                        if len(row) > max(codice_idx, punteggio_idx):
                            codice = row[codice_idx]
                            punteggio = row[punteggio_idx]
                            
                            # Clean up the data (remove extra spaces/newlines)
                            if codice:
                                codice = codice.strip()
                            if punteggio:
                                punteggio = punteggio.strip()
                                
                            # Add the extracted data to our list
                            if codice and punteggio:
                                all_data.append([codice, punteggio])
                        else:
                            print(f"Skipping malformed row: {row}")

            return all_data

    except FileNotFoundError:
        print(f"Error: The file '{pdf_file_path}' was not found.")
        print("Please make sure the file is in the same directory or provide the full path.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def write_to_csv(data, output_file_path):
    """
    Writes the extracted data to a CSV file.
    """
    if not data:
        print("No data was extracted to write to CSV.")
        return
        
    print(f"\nWriting {len(data)} records to {output_file_path}...")
    
    try:
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row
            #writer.writerow([HEADER_1, HEADER_2])
            
            # Write all the data rows
            writer.writerows(data)
            
        print("Successfully created CSV file!")
    except IOError:
        print(f"Error: Could not write to file '{output_file_path}'.")
        print("Please check file permissions.")
    except Exception as e:
        print(f"An error occurred while writing CSV: {e}")

# --- Main execution ---
if __name__ == "__main__":
    if pdf_path == 'your_file.pdf':
        print("Error: Please update the 'pdf_path' variable in the script to point to your PDF file.")
        sys.exit(1)
        
    extracted_data = extract_data_from_pdf(pdf_path)
    
    if extracted_data is not None:
        write_to_csv(extracted_data, csv_path)