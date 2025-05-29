import pandas as pd
import re

def clean_abstract_records(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Remove rows where abstract length is less than 100
    df = df[df['abstract'].str.len() >= 100]
    
    # Remove rows with invalid characters in abstract
    # Keep only alphanumeric, spaces and basic punctuation
    valid_pattern = r'^[a-zA-Z0-9\s.,!?()-:;\'\"]+$'
    df = df[df['abstract'].str.match(valid_pattern)]
    
    # Remove rows where abstract doesn't start with an English letter
    df = df[df['abstract'].str.match(r'^[a-zA-Z]')]
    
    # Save the cleaned data to new CSV
    df.to_csv(output_csv, index=False)
    
if __name__ == "__main__":
    input_file = "datasource/threshold97/threshold_97.csv"  # Replace with your input file name
    output_file = "datasource/cleaned/threshold_clean_97.csv"  # Replace with desired output file name
    clean_abstract_records(input_file, output_file)

