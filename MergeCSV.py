import os
import glob
import pandas as pd
from datetime import datetime

# Set the directory where your CSV files are located
directory = "C:\\Users\\jesse\\Desktop\\DDHW\\CSV_and_JSON\\Bitcoin"  # Replace with your directory path

# List all CSV files in the directory
csv_files = glob.glob(os.path.join(directory, "*.csv"))

# Create an empty list to store DataFrames
dataframes = []

# Iterate through CSV files and handle exceptions
for file in csv_files:
    try:
        df = pd.read_csv(file)
        dataframes.append(df)
    except Exception as e:
        print(f"Error while reading {file}: {str(e)}")

# Check if any CSV files were successfully read
if not dataframes:
    print("No valid CSV files found in the specified directory.")
else:
    # Concatenate all DataFrames into one
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Sort the merged DataFrame by 'Username' and 'Timestamp'
    sorted_df = merged_df.sort_values(by=['Username', 'Timestamp'])

    # Generate the output filename with the current date
    current_date = datetime.now().strftime("%Y%m%d")
    output_csv = f"C:\\Users\\jesse\\Desktop\\DDHW\\Processing\\{current_date}_merged_data.csv"

    # Save the sorted DataFrame to the new CSV file
    sorted_df.to_csv(output_csv, index=False)

    print(f'Merged and sorted data saved to {output_csv}')
